clc 
clear all

%读入数据
yi = 0: 38.2: 38.2*2912;
xi = 0: 38.2: 38.2*2774;
z = xlsread('C:\Users\mengw\Desktop\2017-数学建模大赛\2017年试题\A\附件1 区域高程数据.xlsx');
z=z';

%surf(x, y, z)
for n=1:1:2775
    for m=1:1:2913
       if z(m,n)<3000
          z(m,n)=11.11;  
       end 
    end
end 

%sareamatrix=zeros(33,33);
%生成87*91的面积矩矩阵,矩阵数据坐标为（ax,ay）,(ax,ay)上下左右边线分别为32ay+1,32ay-31,32ax-31,32ax+1;
sarea=zeros(91,87);
for bucg=1:1:10
    z(:,2775+bucg)=0;
end
length(z(1,:))

for i=1:1:91
    for j=1:1:87
       %sareamatrix=zeros(33,33);
       sareamatrix=z(i*32-31:i*32+1,j*32-31:j*32+1);
       numx1=0;numx2=0;
       numx3=0;numx4=0;numx5=0;
     for num=1:1:33
       numx1=length(find(sareamatrix(num,:)==11.11))+numx1;
     end
       numx2=length(find(sareamatrix(1,:)==11.11));
       numx3=length(find(sareamatrix(33,:)==11.11));
       numx4=length(find(sareamatrix(:,1)==11.11));
       numx5=length(find(sareamatrix(:,33)==11.11));
       sarea(j,i)=numx1*38.2*38.2-(numx2+numx3+numx4+numx5)*38.2*38.2*0.5;
    end
end

    %距离（110,0)-1点的距离矩阵，距离（110，50）-2点的距离矩阵
    areamT1=0;
    areamT2=0;
    for i=1:1:91
        for j=1:1:87
            distance_1(i,j)=((16*38.2*j-110000)^2+(16*38.2*i)^2)^(1/2);
            areamT1=sarea(i,j)*distance_1(i,j)+areamT1;
            %distance_2(i,j)=((16*38.2*j-110000)^2+(16*38.2*i-50000)^2)^(1/2);
            %areamT2=sarea(i,j)*distance_2(i,j)+areamT2;
        end
    end
    areamT1
    areamT2
%distance_1
%distance_2




%从（110,0）点放飞SUV1
%寻找最近距离
% distance_1_nearest=200000;
% distance_2_nearest=200000;
% %{    for i=1:1:91
%         for j=1:1:87
%             if sarea(i,j)~=0
%                 if distance_1(i,j)<distance_1_nearest
%                     distance_1_nearest=distance_1(i,j);  %将最近的距离赋给distanc_1_nearest
%                     N1=(i,j);                            %将该点的坐标赋给N1
%                 end
%                if distance_2(i,j)<distance_2_nearest
%                   distance_2_nearest=distance_2(i,j);  %将最近的距离赋给distanc_2_nearest
%                    N2=(i,j);                            %将该点的坐标赋给N2
%                end
%             end
%         end
%         end  
% 

