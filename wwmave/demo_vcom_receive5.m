% 仿 main_pplcount_viz.m 写一个接收指令的接口
%{
读取配置
检索端口
启动端口
接收数据
处理数据
存储数据
...
结束并关闭
%}
%% 清理端口
close_serial();
if(exist('mongoCol'))
    fprintf('重复');
    clear all
end
%% 初始化数据
handles=struct();
handles.angle = 0;
maxNumTracks = 20; % trackingHist组件1行20列的矩阵
lostSync = 0; % h99
frameNum = 1; % h102  ？帧从1开始
maxBytesAvailable = 0;
gotHeader = 0;
trackerRun = 'Target';
peopleCountTotal=0;
outOfSyncBytes = 0; % 出错判断
reason='no problem';

%% 读取配置
cfgfilename='mmw_pplcount_demo_default.cfg';
cliCfg = readCfg(cfgfilename);
[Params cliCfg] = parseCfg(cliCfg, handles.angle); 


%% 获取端口号
[strPorts numPorts] = get_com_ports();
%UserUART = struct('strPort', strPorts{1,1}, 'comNum', numPorts(1,1));
UserData = struct('strPort', strPorts{1,2}, 'comNum', numPorts(1,2));
hDataSerialPort = configureDataSport(UserData.strPort, 65536);

%% 数据存储方式
sceneDb= Params.devCfg.seledb;
% mongo 若是存在则清除，需要重建
if( strcmp(sceneDb,'mongo'))
    
    % 当出现异常则跳转到记事本存储，并通知管理员 
    dbpath=strcat(pwd,'\mongo-java-driver-3.2.2.jar');
    %dbpath=strcat(pwd,'\mongo-java-driver-3.11.0.jar');
    javaaddpath(dbpath)
    import com.mongodb.*
    mongoUri=MongoClientURI(Params.dbDev.uri); 
    mongoC=MongoClient(mongoUri); %//实例化 mongo连接
    mongoDb=mongoC.getDB(Params.dbDev.db); %//连接 db数据库
    mongoCol=mongoDb.getCollection(Params.dbDev.col); %//连接
    writecon=com.mongodb.WriteConcern(1);
    
end
% sqlite
if(strcmp(sceneDb,'sqlite'))
    % 当出现异常则跳转到记事本存储，并通知管理员
    dbpath=strcat(pwd,'\fhistRT.db'); % 需要替换位 sqlit
    %sql_exec='select count(*) from trace_point';
    javaFileName=java.io.File(dbpath);
    dbsqlite = com.almworks.sqlite4java.SQLiteConnection(javaFileName);
    dbsqlite.open(1);
    % 调用sql执行
    %java.lang.System.out.println(st.columnValue(0)); % 打印一条记录
    %st.dispose();
    %db.dispose();
end
% fdtxt
if(strcmp(sceneDb,'fdtxt'))
    sjfid=fopen('serial_data.txt','w+');
    %fclose(fid) %关闭fid窗口    
end


%% 定义数据包的结构体
%{ 
   一个帧中包含哪些数据

%}
syncPatternUINT64 = typecast(uint16([hex2dec('0102'),hex2dec('0304'),hex2dec('0506'),hex2dec('0708')]),'uint64');
syncPatternUINT8 = typecast(uint16([hex2dec('0102'),hex2dec('0304'),hex2dec('0506'),hex2dec('0708')]),'uint8');

frameHeaderStructType = struct(...
    'sync',             {'uint64', 8}, ... % See syncPatternUINT64 below
    'version',          {'uint32', 4}, ...
    'platform',         {'uint32', 4}, ...
    'timestamp',        {'uint32', 4}, ... % 600MHz clocks
    'packetLength',     {'uint32', 4}, ... % In bytes, including header
    'frameNumber',      {'uint32', 4}, ... % Starting from 1
    'subframeNumber',   {'uint32', 4}, ...
    'chirpMargin',      {'uint32', 4}, ... % Chirp Processing margin, in ms
    'frameMargin',      {'uint32', 4}, ... % Frame Processing margin, in ms
    'uartSentTime' ,    {'uint32', 4}, ... % Time spent to send data, in ms
    'trackProcessTime', {'uint32', 4}, ... % Tracking Processing time, in ms
    'numTLVs' ,         {'uint16', 2}, ... % Number of TLVs in thins frame
    'checksum',         {'uint16', 2});    % Header checksum

tlvHeaderStruct = struct(...
    'type',             {'uint32', 4}, ... % TLV object Type
    'length',           {'uint32', 4});    % TLV object Length, in bytes, including TLV header 

% Point Cloud TLV object consists of an array of points. 
% Each point has a structure defined below
pointStruct = struct(...
    'range',            {'float', 4}, ... % Range, in m
    'angle',            {'float', 4}, ... % Angel, in rad
    'doppler',          {'float', 4}, ... % Doplper, in m/s
    'snr',              {'float', 4});    % SNR, ratio
% Target List TLV object consists of an array of targets. 
% Each target has a structure define below
targetStruct = struct(...
    'tid',              {'uint32', 4}, ... % Track ID
    'posX',             {'float', 4}, ... % Target position in X dimension, m
    'posY',             {'float', 4}, ... % Target position in Y dimension, m
    'velX',             {'float', 4}, ... % Target velocity in X dimension, m/s
    'velY',             {'float', 4}, ... % Target velocity in Y dimension, m/s
    'accX',             {'float', 4}, ... % Target acceleration in X dimension, m/s2
    'accY',             {'float', 4}, ... % Target acceleration in Y dimension, m/s
    'EC',               {'float', 9*4}, ... % Tracking error covariance matrix, [3x3], in range/angle/doppler coordinates
    'G',                {'float', 4});    % Gating function gain

frameHeaderLengthInBytes = lengthFromStruct(frameHeaderStructType); %帧头52, 
tlvHeaderLengthInBytes = lengthFromStruct(tlvHeaderStruct); % tlv头8, 
pointLengthInBytes = lengthFromStruct(pointStruct); % 点云16, 
targetLengthInBytes = lengthFromStruct(targetStruct); %目标68
indexLengthInBytes = 1;
fprintf('%d, %d, %d, %d, %d', frameHeaderLengthInBytes, tlvHeaderLengthInBytes, pointLengthInBytes, targetLengthInBytes, indexLengthInBytes)

frameStatStruct = struct('targetFrameNum', [], 'bytes', [], 'numInputPoints', 0, 'numOutputPoints', 0, 'timestamp', 0, 'start', 0, 'benchmarks', [], 'done', 0, ...
    'pointCloud', [], 'targetList', [], 'indexArray', []);
fHist = repmat(frameStatStruct, 1, 10000);

trackingHistStruct = struct('tid', 0, 'allocationTime', 0, 'tick', 0, 'posIndex', 0, 'histIndex', 0, 'sHat', zeros(1000,6), 'ec', zeros(1000,9),'pos', zeros(100,2), 'hMeshU', [], 'hMeshG', [], 'hPlotAssociatedPoints', [], 'hPlotTrack', [], 'hPlotCentroid', []);
trackingHist = repmat(trackingHistStruct, 1, maxNumTracks); %repmat(A, x,y)重复数组副本。 x行y列的重复A

%% 二次定义数据
wall = Params.wall;
scene.areaBox = [wall.left wall.back abs(wall.left)+wall.right wall.front+abs(wall.back)];


%% 读取数据
while(isvalid(hDataSerialPort))

    
    while(lostSync == 0 && isvalid(hDataSerialPort))

        sjlooptime = posixtime(datetime())*1000 - 8*60*60*1000;% 时间戳 毫秒
        frameStart = tic;
        fHist(frameNum).timestamp = frameStart;
        bytesAvailable = get(hDataSerialPort,'BytesAvailable');
        if(bytesAvailable > maxBytesAvailable)
            maxBytesAvailable = bytesAvailable;
        end
        fprintf('bytesAvailable %d \n', bytesAvailable)
        
        fHist(frameNum).bytesAvailable = bytesAvailable;
        if(gotHeader == 0)
            %Read the header first
            [rxHeader, byteCount] = fread(hDataSerialPort, frameHeaderLengthInBytes, 'uint8');
        end
        fHist(frameNum).start = 1000*toc(frameStart);
        
        magicBytes = typecast(uint8(rxHeader(1:8)), 'uint64');
        if(magicBytes ~= syncPatternUINT64)
            reason = 'No SYNC pattern';
            lostSync = 1;
            break;
        end
        if(byteCount ~= frameHeaderLengthInBytes)
            reason = 'Header Size is wrong';
            lostSync = 1;
            break;
        end        
        if(validateChecksum(rxHeader) ~= 0)
            reason = 'Header Checksum is wrong';
            lostSync = 1;
            break; 
        end
        
        frameHeader = readToStruct(frameHeaderStructType, rxHeader);
        
        if(gotHeader == 1)
            if(frameHeader.frameNumber > targetFrameNum)
                targetFrameNum = frameHeader.frameNumber;
                disp(['Found sync at frame ',num2str(targetFrameNum),'(',num2str(frameNum),'), after ', num2str(1000*toc(lostSyncTime),3), 'ms']);
                gotHeader = 0;
            else
                reason = 'Old Frame';
                gotHeader = 0;
                lostSync = 1;
                break;
            end
        end
        
        % We have a valid header
        targetFrameNum = frameHeader.frameNumber;
        fHist(frameNum).targetFrameNum = targetFrameNum;
        fHist(frameNum).header = frameHeader;
        
        dataLength = frameHeader.packetLength - frameHeaderLengthInBytes;
        
        fHist(frameNum).bytes = dataLength; 
        numInputPoints = 0;
        numTargets = 0;
        mIndex = [];

        if(dataLength > 0)
            %Read all packet
            [rxData, byteCount] = fread(hDataSerialPort, double(dataLength), 'uint8');
            if(byteCount ~= double(dataLength))
                reason = 'Data Size is wrong'; 
                lostSync = 1;
                break;  
            end
            offset = 0;
    
            fHist(frameNum).benchmarks(1) = 1000*toc(frameStart);

            % TLV Parsing
            for nTlv = 1:frameHeader.numTLVs
                tlvType = typecast(uint8(rxData(offset+1:offset+4)), 'uint32');
                tlvLength = typecast(uint8(rxData(offset+5:offset+8)), 'uint32');
                if(tlvLength + offset > dataLength)
                    reason = 'TLV Size is wrong';
                    lostSync = 1;
                    break;                    
                end
                offset = offset + tlvHeaderLengthInBytes;
                valueLength = tlvLength - tlvHeaderLengthInBytes;
                switch(tlvType)
                    case 6
                        % Point Cloud TLV
                        numInputPoints = valueLength/pointLengthInBytes;
                        if(numInputPoints > 0)                        
                            % Get Point Cloud from the sensor
                            p = typecast(uint8(rxData(offset+1: offset+valueLength)),'single');

                            pointCloud = reshape(p,4, numInputPoints);    
%                            pointCloud(2,:) = pointCloud(2,:)*pi/180;

                            posAll = [pointCloud(1,:).*sin(pointCloud(2,:)); pointCloud(1,:).*cos(pointCloud(2,:))];
                            snrAll = pointCloud(4,:);

                            % Remove out of Range, Behind the Walls, out of FOV points
                            
                            inRangeInd = (pointCloud(1,:) > 1) & (pointCloud(1,:) < 6) & ...
                                (pointCloud(2,:) > -50*pi/180) &  (pointCloud(2,:) < 50*pi/180) & ...
                                (posAll(1,:) > scene.areaBox(1)) & (posAll(1,:) < (scene.areaBox(1) + scene.areaBox(3))) & ...
                                (posAll(2,:) > scene.areaBox(2)) & (posAll(2,:) < (scene.areaBox(2) + scene.areaBox(4)));
                            pointCloudInRange = pointCloud(:,inRangeInd);
                            posInRange = posAll(:,inRangeInd);
%{
                            % Clutter removal
                            staticInd = (pointCloud(3,:) == 0);        
                            clutterInd = ismember(pointCloud(1:2,:)', clutterPoints', 'rows');
                            clutterInd = clutterInd' & staticInd;
                            clutterPoints = pointCloud(1:2,staticInd);
                            pointCloud = pointCloud(1:3,~clutterInd);
%}
                            numOutputPoints = size(pointCloud,2);                          
                        end                        
                        offset = offset + valueLength;
                                            
                    case 7
                        % Target List TLV
                        numTargets = valueLength/targetLengthInBytes;                        
                        TID = zeros(1,numTargets);
                        S = zeros(6, numTargets);
                        EC = zeros(9, numTargets);
                        G = zeros(1,numTargets);                        
                        for n=1:numTargets
                            TID(n)  = typecast(uint8(rxData(offset+1:offset+4)),'uint32');      %1x4=4bytes
                            S(:,n)  = typecast(uint8(rxData(offset+5:offset+28)),'single');     %6x4=24bytes
                            EC(:,n) = typecast(uint8(rxData(offset+29:offset+64)),'single');    %9x4=36bytes
                            G(n)    = typecast(uint8(rxData(offset+65:offset+68)),'single');    %1x4=4bytes
                            offset = offset + 68;
                        end
                         % 不能一帧一帧增加数据，需要一次性增加多条数据
                            %fprintf('\nsj657...%d, %d, %d, %d, %d, %d \n', numTargets, TID(n), S(1), S(2), sjlooptime,targetFrameNum)
                            if( strcmp(sceneDb,'mongo'))
                                mongodoc=BasicDBObject(); %每帧，每秒一个 新的ObjectID 如何处理异常
                                writeMongoClient(mongoCol,writecon,mongodoc, Params.devCfg, peopleCountTotal, TID(n), S(1), S(2), sjlooptime,targetFrameNum)
                            end
                            if( strcmp(sceneDb,'sqlite'))
                                writeSqliteClient(dbsqlite, Params.devCfg.v, peopleCountTotal, TID(n), S(1), S(2), sjlooptime,targetFrameNum);
                            end
                            if( strcmp(sceneDb,'fdtxt'))
                                writeFdtxt(sjfid, Params.devCfg, peopleCountTotal, TID(n), S(1), S(2), sjlooptime,targetFrameNum);
                            end
                        
                        
                    case 8
                        % Target Index TLV
                        numIndices = valueLength/indexLengthInBytes;
                        mIndex = typecast(uint8(rxData(offset+1:offset+numIndices)),'uint8');
                        offset = offset + valueLength;
                end
            end
        end
       
        if(numInputPoints == 0)
            numOutputPoints = 0;
            pointCloud = single(zeros(4,0));
            posAll = [];
            posInRange = [];  
        end
        if(numTargets == 0)
            TID = [];
            S = [];
            EC = [];
            G = [];
        end
        
        fHist(frameNum).numInputPoints = numInputPoints;
        fHist(frameNum).numOutputPoints = numOutputPoints;    
        fHist(frameNum).numTargets = numTargets;
        fHist(frameNum).pointCloud = pointCloud;
        fHist(frameNum).targetList.numTargets = numTargets;
        fHist(frameNum).targetList.TID = TID;
        fHist(frameNum).targetList.S = S;
        
        fHist(frameNum).targetList.G = G;
        fHist(frameNum).indexArray = mIndex;
       
        % Plot pointCloud
        fHist(frameNum).benchmarks(2) = 1000*toc(frameStart);
  
        
        % Delete previous points
        
        
%{        
        if(size(posInRange,2))
            % Cross out Clutter
            hPlotCloudHandleClutter = plot(trackingAx, posInRange(1,clutterInd), posInRange(2,clutterInd), 'xk');
            % Indicate Static
            hPlotCloudHandleStatic = plot(trackingAx, posInRange(1,staticInd & ~clutterInd), posInRange(2,staticInd & ~clutterInd), 'ok');
            % Indicate Dynamic
            hPlotCloudHandleDynamic = plot(trackingAx, posInRange(1,~staticInd), posInRange(2,~staticInd), 'ob');
        end
%}        
        fHist(frameNum).benchmarks(3) = 1000*toc(frameStart);

        switch trackerRun
            case 'Target'
                if(numTargets == 0)
                    TID = zeros(1,0);
                    S = zeros(6,0);
                    EC = zeros(9,0);
                    G = zeros(1,0);
                end
        end
        
        fHist(frameNum).benchmarks(4) = 1000*toc(frameStart);
        
        if nnz(isnan(S))
            reason = 'Error: S contains NaNs';
            lostSync = 1;
            break;
        end
        if nnz(isnan(EC))
            reason = 'Error: EC contains NaNs';
            lostSync = 1;
            break;
        end
        
        tNumC = length(TID);
        peopleCountTotal = tNumC;
        % 超出范围后如何处理
        % 1.
        frameNum = frameNum + 1;
        if(frameNum > 10000)
            frameNum = 1;
        end
        
    end
    
    % 错误数据处理
    % 2.
    if(targetFrameNum)
        lostSyncTime = tic;
        bytesAvailable = get(hDataSerialPort,'BytesAvailable');
        disp(['Lost sync at frame ', num2str(targetFrameNum),'(', num2str(frameNum), '), Reason: ', reason, ', ', num2str(bytesAvailable), ' bytes in Rx buffer']);
    else
        errordlg('Port sync error: Please close and restart program');
    end
    % 3.
    while(lostSync)
        for n=1:8
            [rxByte, byteCount] = fread(hDataSerialPort, 1, 'uint8');
            if(rxByte ~= syncPatternUINT8(n))
                outOfSyncBytes = outOfSyncBytes + 1;
                break;
            end
        end
        if(n == 8)
            lostSync = 0;
            frameNum = frameNum + 1;
            if(frameNum > 10000)
                frameNum = 1;
            end

            [header, byteCount] = fread(hDataSerialPort, frameHeaderLengthInBytes - 8, 'uint8');
            rxHeader = [syncPatternUINT8'; header]; % X=[X; Y] 表示X储存每一次Y的结果，第一次为X=[Y1]， 第二次为X=[Y1; Y2]
            byteCount = byteCount + 8;
            gotHeader = 1;
        end
    end
end



%% 函数区块

% 读取配置
function config = readCfg(filename)
    config = cell(1,100);
    fid = fopen(filename, 'r');
    if fid == -1
        fprintf('File %s not found!\n', filename);
        return;
    else
        fprintf('Opening configuration file %s ...\n', filename);
    end
    tline = fgetl(fid);
    k=1;
    while ischar(tline)
        config{k} = tline;
        tline = fgetl(fid);
        k = k + 1;
    end
    config = config(1:k-1);
    fclose(fid);
end

% 开启端口
function [sphandle] = configureDataSport(comPortString, bufferSize)
  
    %comPortString = ['COM' num2str(comPortNum)];
    sphandle = serial(comPortString,'BaudRate',921600);
    set(sphandle,'Terminator', '');
    set(sphandle,'InputBufferSize', bufferSize);
    set(sphandle,'Timeout',20);
    set(sphandle,'ErrorFcn',@dispError);
    fopen(sphandle);
end

%  获取com 口
function [strPorts numPorts] = get_com_ports()
    % window 命令行 wmic 获取com设备列表
    command = 'wmic path win32_pnpentity get caption /format:list | find "COM"';
    [status, cmdout] = system (command);
    UART_COM = regexp(cmdout, 'UART\s+\(COM[0-9]+', 'match');
    UART_COM = (regexp(UART_COM, 'COM[0-9]+', 'match'));
    DATA_COM = regexp(cmdout, 'Data\s+Port\s+\(COM[0-9]+', 'match');
    DATA_COM = (regexp(DATA_COM, 'COM[0-9]+', 'match'));
    
    n = length(UART_COM);
    if (n==0)
        errordlg('Error: No Device Detected')
        return
    else
        CLI_PORT = zeros(n,1);
        S_PORT = zeros(n,1);
        strPorts = {};
        for i=1:n
            temp = cell2mat(UART_COM{1,i});
            strPorts{i,1} = temp;
            CLI_PORT(i,1) = str2num(temp(4:end));
            temp = cell2mat(DATA_COM{1,i});
            strPorts{i,2} = temp;
            S_PORT(i,1) = str2num(temp(4:end));
        end

        CLI_PORT = sort(CLI_PORT);
        S_PORT = sort(S_PORT);
        numPorts = [CLI_PORT, S_PORT];
    end
end
% 关闭端口
function close_main()
    %helpdlg('Saving and closing'); 
    open_port = instrfind('Type','serial','Status','open');
    for i=1:length(open_port)
        fclose(open_port(i));
        delete(open_port(i));
    end
    clear all     
end

% 读取配置文件
function [P, cliCfg] = parseCfg(cliCfg, azimuthTilt)
    P=[];
    for k=1:length(cliCfg)
        C = strsplit(cliCfg{k});
        if strcmp(C{1},'channelCfg')
            P.channelCfg.txChannelEn = str2double(C{3});
            P.dataPath.numTxAzimAnt = bitand(bitshift(P.channelCfg.txChannelEn,0),1) +...
                                      bitand(bitshift(P.channelCfg.txChannelEn,-1),1);
            P.dataPath.numTxElevAnt = 0;
            P.channelCfg.rxChannelEn = str2double(C{2});
            P.dataPath.numRxAnt = bitand(bitshift(P.channelCfg.rxChannelEn,0),1) +...
                                  bitand(bitshift(P.channelCfg.rxChannelEn,-1),1) +...
                                  bitand(bitshift(P.channelCfg.rxChannelEn,-2),1) +...
                                  bitand(bitshift(P.channelCfg.rxChannelEn,-3),1);
            P.dataPath.numTxAnt = P.dataPath.numTxElevAnt + P.dataPath.numTxAzimAnt;
                                
        elseif strcmp(C{1},'trackingCfg')
            % error check for azimuth tilt
            % if cfg tilt is not same as GUI specified tilt; GUI specified
            % tilt is used instead
            
            if((str2num(C{8})-90)*pi/180 ~= azimuthTilt)
                temp = cliCfg{k};
                temp(end+1-length(C{8}):end) = '';
                ang = num2str(90-azimuthTilt);
                temp = [temp ang];
                cliCfg{k} = temp;
                
                fprintf('--->trackingCfg specifies %d.\n', (str2num(C{8})-90)*pi/180 );
                fprintf('GUI specifies %d. %s will be used for azimuth in cfg.\n',azimuthTilt, ang);
            end
        elseif strcmp(C{1},'profileCfg')
            P.profileCfg.startFreq = str2double(C{3});
            P.profileCfg.idleTime =  str2double(C{4});
            P.profileCfg.rampEndTime = str2double(C{6});
            P.profileCfg.freqSlopeConst = str2double(C{9});
            P.profileCfg.numAdcSamples = str2double(C{11});
            P.profileCfg.digOutSampleRate = str2double(C{12}); %uints: ksps
        elseif strcmp(C{1},'devCfg')
            P.devCfg.v = str2double(C{2});
            P.devCfg.offtrackX = str2double(C{3});
            P.devCfg.offtrackY = str2double(C{4});
            P.devCfg.seledb = C{5};
        elseif strcmp(C{1},'dbDev')
            P.dbDev.uri = C{2};
            P.dbDev.db = C{3};
            P.dbDev.col = C{4};
        elseif strcmp(C{1},'SceneryParam')
            P.wall.left = str2double(C{2}); 
            P.wall.right = str2double(C{3}); 
            P.wall.front = str2double(C{4}); 
            P.wall.back = str2double(C{5});
        elseif strcmp(C{1},'chirpCfg')
        elseif strcmp(C{1},'frameCfg')
            P.frameCfg.chirpStartIdx = str2double(C{2});
            P.frameCfg.chirpEndIdx = str2double(C{3});
            P.frameCfg.numLoops = str2double(C{4});
            P.frameCfg.numFrames = str2double(C{5});
            P.frameCfg.framePeriodicity = str2double(C{6});
        elseif strcmp(C{1},'guiMonitor')
            P.guiMonitor.detectedObjects = str2double(C{2});
            P.guiMonitor.logMagRange = str2double(C{3});
            P.guiMonitor.rangeAzimuthHeatMap = str2double(C{4});
            P.guiMonitor.rangeDopplerHeatMap = str2double(C{5});
        end
    end
    P.dataPath.numChirpsPerFrame = (P.frameCfg.chirpEndIdx -...
                                            P.frameCfg.chirpStartIdx + 1) *...
                                            P.frameCfg.numLoops;
    P.dataPath.numDopplerBins = P.dataPath.numChirpsPerFrame / P.dataPath.numTxAnt;
    P.dataPath.numRangeBins = pow2roundup(P.profileCfg.numAdcSamples);
    P.dataPath.rangeResolutionMeters = 3e8 * P.profileCfg.digOutSampleRate * 1e3 /...
                     (2 * P.profileCfg.freqSlopeConst * 1e12 * P.profileCfg.numAdcSamples);
    P.dataPath.rangeIdxToMeters = 3e8 * P.profileCfg.digOutSampleRate * 1e3 /...
                     (2 * P.profileCfg.freqSlopeConst * 1e12 * P.dataPath.numRangeBins);
    P.dataPath.dopplerResolutionMps = 3e8 / (2*P.profileCfg.startFreq*1e9 *...
                                        (P.profileCfg.idleTime + P.profileCfg.rampEndTime) *...
                                        1e-6 * P.dataPath.numDopplerBins * P.dataPath.numTxAnt);
end
% 计算最大平方数
function [y] = pow2roundup (x)
    y = 1;
    while x > y
        y = y * 2;
    end
end
% 计算结构体的长度
function length = lengthFromStruct(S)
    fieldName = fieldnames(S);
    length = 0;
    for n = 1:numel(fieldName)
        [~, fieldLength] = S.(fieldName{n}); %获取某字段的长度
        length = length + fieldLength;
    end
end
% 清理端口
function close_serial()
    %helpdlg('Saving and closing'); 
    open_port = instrfind('Type','serial','Status','open');
    for i=1:length(open_port)
        fclose(open_port(i));
        delete(open_port(i));
    end
    clear all 
   
end
% 检查头
function CS = validateChecksum(header)
    h = typecast(uint8(header),'uint16');
    a = uint32(sum(h));
    b = uint16(sum(typecast(a,'uint16')));
    CS = uint16(bitcmp(b));
end


% 拼接sql语句，执行插入数据
function writeSqliteClient(db, pdevid, ppcount, ptid, ps1, ps2, ptim, pframe)
    sql_exec='insert into tracelists("devid", "ppcount", "tid", "sx", "sy", "timeutc","targetframe") values(';
    sql_exec=strcat(sql_exec, num2str(pdevid), ',', num2str(ppcount), ',', num2str(ptid), ',', num2str(ps1), ',', num2str(ps2), ',', num2str(pframe), ',', num2str(ptim), ')');
    st = db.prepare(sql_exec);
    st.step();
    disp(st)
end

% 插入mongo 数据
function writeMongoClient(col, wc,doc, pdevcfg, ppcount, ptid, ps1, ps2, ptim, pframe)
    %fprintf('---mongo--:::%d:::%d :::\n', ps1, ps2)
    % 如何处理异常 offtrackX 是宽度、x的值、芯片右侧的距离， offtrackY是 y值、与后墙的距离
	doc.put('devid', pdevcfg.v);
	doc.put('ppcount', ppcount);
    doc.put('tid', ptid);
	doc.put('sx', (pdevcfg.offtrackX - ps1* 100));
    doc.put('sy', (pdevcfg.offtrackY + ps2 * 100));
	doc.put('timeutc', ptim);
    doc.put('targetframe', pframe)	;
	col.insert(doc,wc);    
end
% 写入记事本
function writeFdtxt(fid, pdevcfg, ppcount, ptid, ps1, ps2, ptim, pframe)
    % offtrackX, offtrackY 为相对位置的偏离值
    
    ps10 =round(pdevcfg.offtrackX - ps1* 100);
    ps20 =round(pdevcfg.offtrackY + ps2 * 100);
    w_col=strcat(num2str(pdevcfg.v), ',', num2str(ppcount), ',', num2str(ptid), ',', num2str(ps10), ',', num2str(ps20), ',', num2str(ptim), ',', num2str(pframe));
    fprintf(fid,'%s\n',w_col);   
end
% 读结构
function [R] = readToStruct(S, ByteArray)
    fieldName = fieldnames(S);
    offset = 0;
    for n = 1:numel(fieldName)
        [fieldType, fieldLength] = S.(fieldName{n});
        R.(fieldName{n}) = typecast(uint8(ByteArray(offset+1:offset+fieldLength)), fieldType);
        offset = offset + fieldLength;
    end
end