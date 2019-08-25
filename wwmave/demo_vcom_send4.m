% 仿 main_pplcount_viz.m 写一个发送指令的接口
%{
读取配置
检索端口
启动端口
发送数据
接收回传
继续发送数据
...
结束并关闭
%}

%读取配置
cfgfilename='mmw_pplcount_demo_default.cfg';
cliCfg = readCfg(cfgfilename);
[strPorts numPorts] = get_com_ports();
UserUART = struct('strPort', strPorts{1,1}, 'comNum', numPorts(1,1));
%UserData = struct('strPort', strPorts{1,2}, 'comNum', numPorts(1,2));
hControlSerialPort = configureControlPort(UserUART.strPort);
mmwDemoCliPrompt = char('mmwDemo:/>');
% 发送指令
for k=1:length(cliCfg)
    fprintf(hControlSerialPort, cliCfg{k}); %默认"%s\n" 格式
    %fprintf('%s\n', cliCfg{k});
    echo = fgetl(hControlSerialPort); % Get an echo of a command
    done = fgetl(hControlSerialPort); % Get "Done" 
    prompt = fread(hControlSerialPort, size(mmwDemoCliPrompt,2)); % Get the prompt back 
end

fclose(hControlSerialPort);
delete(hControlSerialPort);
fprintf('sucess.');


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
end   
%  获取com 口
function [strPorts numPorts] = get_com_ports()
    
    
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