% 有小帧 后面的数据
%%{
frameHeaderLengthInBytes=52;
frameHeader=struct('sync', 506660481457717506,   ...
             'version',33554436,   ...
            'platform', 661058,   ...
           'timestamp', 3061110381,   ...
        'packetLength',236,   ...
         'frameNumber', 239325,   ...
      'subframeNumber', 0,   ...
         'chirpMargin', 78,   ...
         'frameMargin', 20672,   ...
        'uartSentTime', 12,   ...
    'trackProcessTime', 2206,   ...
             'numTLVs', 2,   ...
            'checksum', 18738)
%%}
% packetLength - frameHeaderLengthInBytes= dataLength, 76-52=24
% 数据中包含 点 和 target
rxData2=[6     0     0     0    40     0     0     0   108   214    15    64   146    10     6   190   179    21   166    61   148    75   200    64   108   214    ...
        15    64   219    15   201   189   179    21   166    61    83    85   209    64     7     0     0     0   144     0     0     0    10     0     0  ...
        0   149   211   222   189    81   102   141    63     0     0     0     0    0     0     0     0     0     0     0     0     0     0     0     0    ...
        46   254    13    65    64    91   141    62    50   229   177   190    62    91   141    62   105  252     4    65   134   112   248   187    50   ...
        229   177   190   133   112   248   187   135   210    31    63     0     0   128    63    11     0     0     0   208   102   145   190   229   141 ...
        13    64     0     0     0     0     0     0     0     0     0     0     0     0     0     0    0     0    49   206    52    65    76   182   249   ...
        187  105    81     0   190   166   182  249   187   174   244    64    66   183    50  143   188   105    81     0   190   189    50   143   ...
        188    96   200    84    63     0     0   128    63]
length(rxData2)

% 设置一个循环 ，循环次数 numTLVs 设置位移量 offset为0
% rxData2前8位 是tlv 头
tlvhead=rxData2(1:8)%[6     0     0     0    40     0     0     0 ]
tlvType = typecast(uint8(tlvhead(1:4)), 'uint32');
tlvLength = typecast(uint8(tlvhead(5:8)), 'uint32'); % 40
onePonitvalueLength=tlvLength-8; % 32, 8是一个tlv头的字节数
fprintf('tlvType, %d, tlvLength, %d, onePonitvalueLength, %d \n', tlvType, tlvLength, onePonitvalueLength)

% tlv类型 [6     0     0     0 ] 转为unit 32位
% tlv数量 [24     0     0     0] 转为unit 32位
% tlv数值 [95    88    28    64   219    15   201   189   179    21   166   189   232   157   253    64]
% pointlength = 16,即一个point 共16个字节，由4个元素组成， 每个元素4个字节。
% pointData=rxData2(9:40)
pointData=rxData2(9:40);
p=typecast(uint8(pointData),'single');
disp(p)
pointCloud = reshape(p,4, 2);
disp(pointCloud)
posAll = [pointCloud(1,:).*sin(pointCloud(2,:)); pointCloud(1,:).*cos(pointCloud(2,:))];
disp(posAll)
% 第2个循环
tlvhead2=rxData2(41:48)
tlvType2 = typecast(uint8(rxData2(41:44)), 'uint32');
tlvLength2 = typecast(uint8(rxData2(45:48)), 'uint32'); % 40
targetValueLength=tlvLength2-8; % 136, 8是一个tlv头的字节数
fprintf('tlvType, %d, tlvLength, %d, targetValueLength, %d \n', tlvType2, tlvLength2, targetValueLength)
targetData=rxData2(49:184); % 41开始 144个字节，40+144=184，第184位截至
targetLengthInBytes=68;
numTargets = targetValueLength/targetLengthInBytes;     %目标数 2                   
TID = zeros(1,numTargets);
S = zeros(6, numTargets);
EC = zeros(9, numTargets);
G = zeros(1,numTargets);
offset=48;
for n=1:numTargets
    TID(n)  = typecast(uint8(rxData2(offset+1:offset+4)),'uint32');      %1x4=4bytes
    S(:,n)  = typecast(uint8(rxData2(offset+5:offset+28)),'single');     %6x4=24bytes
    EC(:,n) = typecast(uint8(rxData2(offset+29:offset+64)),'single');    %9x4=36bytes
    G(n)    = typecast(uint8(rxData2(offset+65:offset+68)),'single');    %1x4=4bytes
    offset = offset + 68;
    disp(TID(n))
    disp(S(:,n)); %其中 S1, S2 为坐标x,y
end

