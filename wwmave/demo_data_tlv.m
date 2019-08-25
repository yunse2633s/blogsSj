% ��С֡ ���������
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
% �����а��� �� �� target
rxData2=[6     0     0     0    40     0     0     0   108   214    15    64   146    10     6   190   179    21   166    61   148    75   200    64   108   214    ...
        15    64   219    15   201   189   179    21   166    61    83    85   209    64     7     0     0     0   144     0     0     0    10     0     0  ...
        0   149   211   222   189    81   102   141    63     0     0     0     0    0     0     0     0     0     0     0     0     0     0     0     0    ...
        46   254    13    65    64    91   141    62    50   229   177   190    62    91   141    62   105  252     4    65   134   112   248   187    50   ...
        229   177   190   133   112   248   187   135   210    31    63     0     0   128    63    11     0     0     0   208   102   145   190   229   141 ...
        13    64     0     0     0     0     0     0     0     0     0     0     0     0     0     0    0     0    49   206    52    65    76   182   249   ...
        187  105    81     0   190   166   182  249   187   174   244    64    66   183    50  143   188   105    81     0   190   189    50   143   ...
        188    96   200    84    63     0     0   128    63]
length(rxData2)

% ����һ��ѭ�� ��ѭ������ numTLVs ����λ���� offsetΪ0
% rxData2ǰ8λ ��tlv ͷ
tlvhead=rxData2(1:8)%[6     0     0     0    40     0     0     0 ]
tlvType = typecast(uint8(tlvhead(1:4)), 'uint32');
tlvLength = typecast(uint8(tlvhead(5:8)), 'uint32'); % 40
onePonitvalueLength=tlvLength-8; % 32, 8��һ��tlvͷ���ֽ���
fprintf('tlvType, %d, tlvLength, %d, onePonitvalueLength, %d \n', tlvType, tlvLength, onePonitvalueLength)

% tlv���� [6     0     0     0 ] תΪunit 32λ
% tlv���� [24     0     0     0] תΪunit 32λ
% tlv��ֵ [95    88    28    64   219    15   201   189   179    21   166   189   232   157   253    64]
% pointlength = 16,��һ��point ��16���ֽڣ���4��Ԫ����ɣ� ÿ��Ԫ��4���ֽڡ�
% pointData=rxData2(9:40)
pointData=rxData2(9:40);
p=typecast(uint8(pointData),'single');
disp(p)
pointCloud = reshape(p,4, 2);
disp(pointCloud)
posAll = [pointCloud(1,:).*sin(pointCloud(2,:)); pointCloud(1,:).*cos(pointCloud(2,:))];
disp(posAll)
% ��2��ѭ��
tlvhead2=rxData2(41:48)
tlvType2 = typecast(uint8(rxData2(41:44)), 'uint32');
tlvLength2 = typecast(uint8(rxData2(45:48)), 'uint32'); % 40
targetValueLength=tlvLength2-8; % 136, 8��һ��tlvͷ���ֽ���
fprintf('tlvType, %d, tlvLength, %d, targetValueLength, %d \n', tlvType2, tlvLength2, targetValueLength)
targetData=rxData2(49:184); % 41��ʼ 144���ֽڣ�40+144=184����184λ����
targetLengthInBytes=68;
numTargets = targetValueLength/targetLengthInBytes;     %Ŀ���� 2                   
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
    disp(S(:,n)); %���� S1, S2 Ϊ����x,y
end

