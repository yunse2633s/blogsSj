function varargout = setup(varargin)
% SETUP MATLAB code for setup.fig
%      SETUP, by itself, creates a new SETUP or raises the existing
%      singleton*.
%
%      H = SETUP returns the handle to a new SETUP or the handle to
%      the existing singleton*.
%
%      SETUP('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in SETUP.M with the given input arguments.
%
%      SETUP('Property','Value',...) creates a new SETUP or raises
%      the existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before setup_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to setup_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help setup

% Last Modified by GUIDE v2.5 02-Aug-2019 11:58:15

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @setup_OpeningFcn, ...
                   'gui_OutputFcn',  @setup_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT

% --- Executes just before setup is made visible.
function setup_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to setup (see VARARGIN)

% Choose default command line output for setup
handles.output = hObject;
handles.camIndex = -1;
handles.hDataSerialPort = [];
handles.hControlSerialPort = [];
handles.angle = 0;
handles.cfg = struct('filename', 'mmw_pplcount_demo_default.cfg', 'loaded', 0);
handles.subzone = [];% 分区
%
% 读取配置文件中的长宽
cliCfg = readCfg(handles.cfg.filename);
[Params cliCfg] = parseCfg(cliCfg, handles.angle); 
handles.params = Params;
handles.wall = handles.params.wall;
disp(handles.wall)   
%
%handles.wall = struct('left', -6, 'right', 6, 'front',6, 'back', 0);%左右墙距离


% Update handles structure
guidata(hObject, handles);

initialize_gui(hObject, handles, false);
drawRadarRoom(handles); %绘制雷达房间
%axes1_CreateFcn(hObject, eventdata, handles);
axes2_CreateFcn(hObject, eventdata, handles);

% COM Port Autoconnect comment/uncomment to enable
%btnConnect_Callback(hObject, eventdata, handles);
% Set COM Status
handles = guidata(hObject);
hCOMStatus = findobj('Tag', 'textCOMStatus');
if(~isempty(handles.hControlSerialPort) && ~isempty(handles.hDataSerialPort))
    update = 'COM STATUS: Ports connected';
else
    update = 'COM STATUS: Ports NOT connected';
end
set(hCOMStatus,'String', update); 
% UIWAIT makes setup wait for user response (see UIRESUME)
 uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = setup_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles;



% --- Executes on button press in btnStart.
function btnStart_Callback(hObject, eventdata, handles)
% hObject    handle to btnStart (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% 端口必须是2个，且2个端口都已经连接上
if(length(instrfind('Type','serial', 'Status','open'))>=2 && ~isempty(handles.hControlSerialPort) && ~isempty(handles.hDataSerialPort))
    mmwDemoCliPrompt = char('mmwDemo:/>');
    hControlSerialPort = handles.hControlSerialPort;

    % load cfg 
    % Read Chirp Configuration file
    cliCfg = readCfg(handles.cfg.filename);
    [Params cliCfg] = parseCfg(cliCfg, handles.angle); 
    handles.params = Params;
    guidata(hObject, handles);
    %Send CLI configuration to IWR16xx
    fprintf('Sending configuration from %s file to IWR16xx ...\n', handles.cfg.filename);
    %disp(hControlSerialPort);
    for k=1:length(cliCfg)
        %disp(cliCfg{k})
        %fprintf('-----ssss----- \n')
        disp(hControlSerialPort)
        %fprintf(obj,'cmd') 将字符串 cmd 写入到已连接到串行端口对象 obj 的设备。"默认格式为 %s\n",
        fprintf(hControlSerialPort, cliCfg{k}); % 将文本写入设备,将字符串 cliCfg{k} 写入到已连接到串行端口对象 obj 的设备
        
        %fprintf('fprintf ..%s\n', cliCfg{k});
        echo = fgetl(hControlSerialPort); % Get an echo of a command "fgetl" 读取文件中的行，并删除换行符 (等待com口回传数据，否则不退出)
        fprintf('----echo---,%d \n', k)
        disp(echo)
        done = fgetl(hControlSerialPort); % Get "Done" 
        fprintf('----done---,%d \n', k)
        disp(done)
        prompt = fread(hControlSerialPort, size(mmwDemoCliPrompt,2)); % Get the prompt back  返回提示符, size(A,dim) 返回维度 dim 的长度。 这一行可以注释
        % fread(fileID,sizeA) 将文件数据读取到维度为 sizeA 的数组 A 中，并将文件指针定位到最后读取的值之后
        %fprintf('----prompt---,%d \n', size(mmwDemoCliPrompt,2))
        %disp(prompt)
        %fprintf('---.....')
    end
    fclose(hControlSerialPort);  % 为何关闭和删除控制端口 fclose (serial)断开串行端口对象和设备之间的连接
    delete(hControlSerialPort);  % 为何关闭和删除控制端口 delete(obj) 删除指定的对象。
    
    % update output
    editLW_Callback(findobj('Tag', 'editLW'), eventdata, handles);
    editRW_Callback(findobj('Tag', 'editRW'), eventdata, handles);
    editFW_Callback(findobj('Tag', 'editFW'), eventdata, handles);
    editBW_Callback(findobj('Tag', 'editBW'), eventdata, handles);
    editAng_Callback(findobj('Tag', 'editAng'), eventdata, handles)
    setup_OutputFcn(hObject,eventdata,guidata(hObject));  % ？ setup out put fcn 是启动输出函数的意思吗？
    uiresume(gcbf); % "uiresume" 恢复执行已阻止的程序
else
    warndlg('Error: Can not start COM ports not connected. Please select and connect.');
end
    


% --- Executes on button press in btnCancel.
function btnCancel_Callback(hObject, eventdata, handles)
% hObject    handle to btnCancel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
delete(instrfind('Type','serial', 'Status','open'))
initialize_gui(gcbf, handles, true);
close(gcbf)




% --------------------------------------------------------------------
function initialize_gui(fig_handle, handles, isreset)


% Update handles structure
guidata(handles.figure1, handles);





% --- Executes on button press in pushbuttonBrowse. 导入配置表
function pushbuttonBrowse_Callback(hObject, eventdata, handles)
% hObject    handle to pushbuttonBrowse (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
selectFile = findobj('Tag','radiobuttonSelectFile');
if(selectFile.Value)
     % Get Chirp Config File
     [filename, pathname] = ...
     uigetfile('*.cfg','*.*');
     configurationFileName = [pathname filename];
     handles.cfg.filename = configurationFileName;
     if (filename ~= 0)
        % Read Chirp Configuration file
        cliCfg = readCfg(handles.cfg.filename);
        [Params cliCfg] = parseCfg(cliCfg, handles.angle); 
        handles.params = Params;
        guidata(hObject,handles)
        drawRadarRoom(handles);
     end
     guidata(hObject,handles)
end




% --- Executes on selection change in popupUART.
function popupUART_Callback(hObject, eventdata, handles)
% hObject    handle to popupUART (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns popupUART contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupUART

selectIndx = hObject.Value;
menuStrings = hObject.String;
strPort = menuStrings{selectIndx};
comNum = str2num(strPort(4:end));
hObject.UserData = struct('strPort', strPort, 'comNum', comNum);


% --- Executes during object creation, after setting all properties.
function popupUART_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupUART (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
[strPorts numPorts] = get_com_ports();
hObject.String = strPorts{:,1};
hObject.UserData = struct('strPort', strPorts{1,1}, 'comNum', numPorts(1,1));




% --- Executes on selection change in popupData.
function popupData_Callback(hObject, eventdata, handles)
% hObject    handle to popupData (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns popupData contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupData

selectIndx = hObject.Value;
menuStrings = hObject.String;
strPort = menuStrings{selectIndx};
comNum = str2num(strPort(4:end));
hObject.UserData = struct('strPort', strPort, 'comNum', comNum);


% --- Executes during object creation, after setting all properties.
function popupData_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupData (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
[strPorts numPorts] = get_com_ports();
hObject.String = strPorts{:,2};
hObject.UserData = struct('strPort', strPorts{1,2}, 'comNum', numPorts(1,2));

% --- Executes on button press in btnConnect. 在btnConnect中按下按钮执行
function btnConnect_Callback(hObject, eventdata, handles)
% hObject    handle to btnConnect (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

hUARTPort = findobj('Tag','editUART'); % findobj "查找具有特定属性的图形对象",或 "查找句柄对象"
hDataPort = findobj('Tag','editDATA');
%disp(hDataPort)
%disp(hUARTPort.UserData)
controlSerialPort = hUARTPort.UserData.strPort;
dataSerialPort = hDataPort.UserData.strPort;

% Clear ports 'isempty':确定数组是否为空, 'instrfind':将串行端口对象从内存读入到 MATLAB 工作区
if ~isempty(instrfind('Type','serial'))
    disp('Serial port(s) already open. Re-initializing...'); % 'disp': 显示变量的值
    delete(instrfind('Type','serial'));  % delete open serial ports.  'delete': 删除文件或对象
end
% Configure data UART port with input buffer to hold 100+ frames 
hDataSerialPort = configureDataSport(dataSerialPort, 65536); %configureDataSport 自定义函数
hControlSerialPort = configureControlPort(controlSerialPort);
handles.hDataSerialPort = hDataSerialPort;
handles.hControlSerialPort = hControlSerialPort;
hCOMStatus = findobj('Tag', 'textCOMStatus');
update = 'COM STATUS: Ports connected';
set(hCOMStatus,'String', update); 
guidata(hObject,handles); % "guidata" :存储或检索 UI 数据


function editLW_Callback(hObject, eventdata, handles)
% hObject    handle to editLW (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editLW as text
%        str2double(get(hObject,'String')) returns contents of editLW as a double
handles.wall.left = -1*str2double(get(hObject,'String'));
guidata(hObject,handles);
drawRadarRoom(handles); % 绘制雷达房
h = guidata(hObject);
fprintf('left wall: %d \n', h.wall.left)

% --- Executes during object creation, after setting all properties.
function editLW_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editLW (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

handles.wall.left = -1*str2double(get(hObject,'String'));
guidata(hObject,handles);




function editRW_Callback(hObject, eventdata, handles)
% hObject    handle to editRW (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editRW as text
%        str2double(get(hObject,'String')) returns contents of editRW as a double
handles.wall.right = str2double(get(hObject,'String'));
guidata(hObject,handles);
drawRadarRoom(handles); % 绘制雷达房
h = guidata(hObject);
fprintf('R wall: %d \n', h.wall.right)

% --- Executes during object creation, after setting all properties.
function editRW_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editRW (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

handles.wall.right = str2double(get(hObject,'String'));
guidata(hObject,handles);



function editBW_Callback(hObject, eventdata, handles)
% hObject    handle to editBW (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editBW as text
%        str2double(get(hObject,'String')) returns contents of editBW as a double
handles.wall.back = -1*str2double(get(hObject,'String'));
guidata(hObject,handles);
drawRadarRoom(handles); % 绘制雷达房间
h = guidata(hObject);
fprintf('back wall: %d \n', h.wall.back)

% --- Executes during object creation, after setting all properties.
function editBW_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editBW (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

handles.wall.back = -1*str2double(get(hObject,'String'));
guidata(hObject,handles);



function editFW_Callback(hObject, eventdata, handles)
% hObject    handle to editFW (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editFW as text
%        str2double(get(hObject,'String')) returns contents of editFW as a double
handles.wall.front = str2double(get(hObject,'String'));
guidata(hObject,handles);
drawRadarRoom(handles); % 绘制雷达房间
h = guidata(hObject);
fprintf('front wall: %d \n', h.wall.front)


% --- Executes during object creation, after setting all properties.
function editFW_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editFW (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

handles.wall.front = str2double(get(hObject,'String'));
guidata(hObject,handles);



function editAng_Callback(hObject, eventdata, handles)
% hObject    handle to editAng (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editAng as text
%        str2double(get(hObject,'String')) returns contents of editAng as a double
handles.angle = str2double(get(hObject,'String'));
guidata(hObject,handles);
drawRadarRoom(handles); %绘制雷达房间


% --- Executes during object creation, after setting all properties.
function editAng_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editAng (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes during object creation, after setting all properties.
function axes1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to axes1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
imshow('images/setupfig.jpg','Parent',handles.axes1);
% Hint: place code in OpeningFcn to populate axes1


% --- Executes during object creation, after setting all properties.
function axes2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to axes2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
imshow('images/angle.jpg','Parent',handles.axes2);
% Hint: place code in OpeningFcn to populate axes2



% --- Executes on button press in radiobuttonSelectFile.
function radiobuttonSelectFile_Callback(hObject, eventdata, handles)
% hObject    handle to radiobuttonSelectFile (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobuttonSelectFile


% --- Executes on button press in radiobuttonUseDefault.
function radiobuttonUseDefault_Callback(hObject, eventdata, handles)
% hObject    handle to radiobuttonUseDefault (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobuttonUseDefault
if(hObject.Value)
     % Get Chirp Config File
     handles.cfg.filename = 'mmw_pplcount_demo_default.cfg';
     guidata(hObject,handles)
end

% 读取配置文件中的信息
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
                fprintf('trackingCfg specifies %d.\n', (str2num(C{8})-90)*pi/180 );
                fprintf('GUI specifies %d. %s will be used for azimuth in cfg.\n',azimuthTilt, ang);
            end
        elseif strcmp(C{1},'profileCfg')
            P.profileCfg.startFreq = str2double(C{3});
            P.profileCfg.idleTime =  str2double(C{4}); %空闲时间
            P.profileCfg.rampEndTime = str2double(C{6}); %斜坡结束时间
            P.profileCfg.freqSlopeConst = str2double(C{9}); % freqSlopeConst :频率斜率常量 ,数值小，探测距离远
            P.profileCfg.numAdcSamples = str2double(C{11}); %numAdcSamples: num Adc样品
            P.profileCfg.digOutSampleRate = str2double(C{12}); %uints: ksps. digOutSampleRate:出样率
            %fprintf('----> %d, %d, %d', str2double(C{9}), str2double(C{11}),str2double(C{12}));
        % 自定义 devCfg:硬件设备号，相对偏离坐标，数据存储方式,
        % dbDev:数据连接符、数据库、表,SceneryParam：自定义房间区域
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

function [y] = pow2roundup (x)
    y = 1;
    while x > y
        y = y * 2;
    end
    
function [sphandle] = configureDataSport(comPortString, bufferSize)
  
    %comPortString = ['COM' num2str(comPortNum)];
    sphandle = serial(comPortString,'BaudRate',921600); %"serial"创建串行端口对象
    set(sphandle,'Terminator', ''); % 设置 "终止符"
    set(sphandle,'InputBufferSize', bufferSize); % 设置 " 缓存区"
    set(sphandle,'Timeout',10); % 设置 "超时"
    set(sphandle,'ErrorFcn',@dispError);
    %fprintf('-------datasport-------');
    %disp(sphandle);
    fopen(sphandle); % " fopen (serial) ":将串行端口对象连接到设备

function [sphandle] = configureControlPort(comPortString)
    %if ~isempty(instrfind('Type','serial'))
    %    disp('Serial port(s) already open. Re-initializing...');
    %    delete(instrfind('Type','serial'));  % delete open serial ports.
    %end
    %comPortString = ['COM' num2str(comPortNum)];
    sphandle = serial(comPortString,'BaudRate',115200);
    set(sphandle,'Parity','none')    
    set(sphandle,'Terminator','LF')        
    fopen(sphandle);

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


% --- Executes when user attempts to close figure1.
function figure1_CloseRequestFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: delete(hObject) closes the figure
delete(hObject);


% --- Executes on selection change in popupWebcam.
function popupWebcam_Callback(hObject, eventdata, handles)
% hObject    handle to popupWebcam (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns popupWebcam contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupWebcam


% --- Executes during object creation, after setting all properties.
function popupWebcam_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupWebcam (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
hObject.String = webcamlist();



% --- Executes on button press in checkbox1.
function checkbox1_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkbox1
if(get(hObject,'Value'))
    hWebcamSelect = findobj('Tag', 'popupWebcam');
    handles.camIndex = hWebcamSelect.Value;
    fprintf('webcam enabled %d', hWebcamSelect.Value)
else
    handles.camIndex = -1;
end
guidata(hObject,handles);

function [strPorts numPorts] = get_com_ports()
    %wmic path win32_pnpentity 获得PCI设备
    command = 'wmic path win32_pnpentity get caption /format:list | find "COM"';
    [status, cmdout] = system (command); %system(command) 调用操作系统执行指定的命令
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
            temp = cell2mat(UART_COM{1,i}); %T_index{i,1}代表取T_index中的第i行第一列的元胞数
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


% --- Executes on button press in checkboxSubzones. 按下复选框子区域中的按钮后执行
function checkboxSubzones_Callback(hObject, eventdata, handles)
% hObject    handle to checkboxSubzones (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkboxSubzones
if(~get(hObject,'Value'))
    handles.subzone = [];
    guidata(hObject,handles);
    drawRadarRoom(handles)
end


function editBox_Callback(hObject, eventdata, handles)
% hObject    handle to editBox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editBox as text
%        str2double(get(hObject,'String')) returns contents of editBox as a double
enableSubzones = get(findobj('Tag', 'checkboxSubzones'),'Value');
if(enableSubzones)
    boxes = str2num(get(hObject,'String'));
    handles.subzone = boxes;
    guidata(hObject,handles);
    drawRadarRoom(handles)
end


% --- Executes during object creation, after setting all properties.
function editBox_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editBox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% 绘制雷达房间
function drawRadarRoom(handles)
ax = handles.axes1;
if ishandle(ax)
    children = get(ax, 'children');
    delete(children);
    scene.azimuthTilt = handles.angle*pi/180;
    wall = handles.wall;
    %sensor parametersv
    if(isfield(handles, 'params'))
        % rangeResolutionMeters：距离分辨率米， numRangeBins：范围 Params.dataPath.numRangeBins*Params.dataPath.rangeIdxToMeters;
        sensor.rangeMax = floor(handles.params.dataPath.numRangeBins*handles.params.dataPath.rangeResolutionMeters);
        fprintf('-setup-> %d <--', sensor.rangeMax)
    else 
        sensor.rangeMax = 6;
    end
    sensor.rangeMin = 1;
    sensor.azimuthFoV = 120*pi/180; %120 degree FOV in horizontal direction
    sensor.angles = linspace(-sensor.azimuthFoV/2, sensor.azimuthFoV/2, 128);
    %hold(ax, 'on')
    plot(ax, sensor.rangeMin*sin(sensor.angles+scene.azimuthTilt), sensor.rangeMin*cos(sensor.angles+scene.azimuthTilt), '-r'); 
    %disp([0,sensor.rangeMax, scene.azimuthTilt, 0])
    %fprintf('---')
    %disp([sensor.rangeMax  sensor.angles scene.azimuthTilt  0])
    plot(ax, [0 sensor.rangeMax*sin(sensor.angles+scene.azimuthTilt) 0],[0 sensor.rangeMax*cos(sensor.angles+scene.azimuthTilt) 0], '-r');
    scene.areaBox = [wall.left wall.back abs(wall.left)+wall.right wall.front+abs(wall.back)];
    
    margin = 0.5; %[m]
    scene.maxPos = [scene.areaBox(1)-margin ...
                    scene.areaBox(1)+scene.areaBox(3)+margin ...
                    scene.areaBox(2)-margin ...
                    scene.areaBox(2)+scene.areaBox(4)+margin];
                %fprintf('----scene.maxPos---')
                %disp(scene.maxPos)
    ax.DataAspectRatio = [1 1 1];
    axis(ax, scene.maxPos);
    ax.CameraUpVector = [0,-1, 0];
    grid(ax, 'on'); % 显示或隐藏坐标区网格线
    grid(ax, 'minor');                
    title(ax, 'Top Down View of Scene'); % 添加标题

    % draw wall box
    rectangle(ax, 'Position', scene.areaBox, 'EdgeColor','k', 'LineStyle', '-', 'LineWidth', 2);
end

% draw target box
colors='brgcm';
numBoxes = size(handles.subzone,1);
for nBoxes = 1:numBoxes
    hTargetBoxHandle(nBoxes)= rectangle('Parent', ax, 'Position', handles.subzone(nBoxes,:), 'EdgeColor', colors(nBoxes), 'LineWidth', 4);
end



function editUART_Callback(hObject, eventdata, handles)
% hObject    handle to popupUART (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of popupUART as text
%        str2double(get(hObject,'String')) returns contents of popupUART as a double
strPort = get(hObject, 'String');
comNum = str2double(strPort(4:end));
hObject.UserData = struct('strPort', strPort, 'comNum', comNum);


% --- Executes during object creation, after setting all properties.
function editUART_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupUART (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
[strPorts numPorts] = get_com_ports();
hObject.String = strPorts{:,1};
hObject.UserData = struct('strPort', strPorts{1,1}, 'comNum', numPorts(1,1))



function editDATA_Callback(hObject, eventdata, handles)
% hObject    handle to popupdata (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of popupdata as text
%        str2double(get(hObject,'String')) returns contents of popupdata as a double
strPort = get(hObject, 'String');
comNum = str2double(strPort(4:end));
hObject.UserData = struct('strPort', strPort, 'comNum', comNum);


% --- Executes during object creation, after setting all properties.
function editDATA_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupdata (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

[strPorts numPorts] = get_com_ports();
hObject.String = strPorts{:,2};
hObject.UserData = struct('strPort', strPorts{1,2}, 'comNum', numPorts(1,2));
