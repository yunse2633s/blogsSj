%结构体定义
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

%初始值 1*n 矩阵，单元格数组 iscell  这组数据是十六转10进制
%{
   rxHeader是fread
%}
rxHeader=[2     1     4     3     6     5     8     7     4     0     0     2    66    22    10     0   206    23    71   179    52     0     0     0   129   200     0     0     0     0     0     0    78     0     0     0   181    80     0     0     1     0     0     0    81     2     0     0     0     0   122   240]

cc = readToStruct(frameHeaderStructType, rxHeader)
% 函数区域
function [R] = readToStruct(S, ByteArray)
    fieldName = fieldnames(S); % 获取结构体中的属性 ,S 是结构体中套结构体 fieldName是一个cell 1*N的数组
    %disp(fieldName)
    offset = 0;
    for n = 1:numel(fieldName) % numel()
        [fieldType, fieldLength] = S.(fieldName{n}); %获取结构体中的属性和规格
        R.(fieldName{n}) = typecast(uint8(ByteArray(offset+1:offset+fieldLength)), fieldType);
        offset = offset + fieldLength;
    end
end
%{ 
%输出结果
                sync: 506660481457717506
             version: 33554436
            platform: 661058
           timestamp: 3007780814
        packetLength: 52
         frameNumber: 51329
      subframeNumber: 0
         chirpMargin: 78
         frameMargin: 20661
        uartSentTime: 1
    trackProcessTime: 593
             numTLVs: 0
            checksum: 61562
%}
%{ 
% 按位分割 获取的数据
2     1     4     3     6     5     8     7     :---:64
4     0     0     2     :---:32
66    22    10     0     :---:32
206    23    71   179     :---:32
52     0     0     0     :---:32
129   200     0     0     :---:32
0     0     0     0     :---:32
78     0     0     0     :---:32
181    80     0     0     :---:32
1     0     0     0     :---:32
81     2     0     0     :---:32
0     0     :---:16
22   240     :---:16

uint64():无符号，占用8个字节。向0方向取整。
uint32():无符号，占用4个字节。向0方向取整。
uint8():无符号，占用1个字节。向0方向取整。
float
%}