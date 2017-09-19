clc 
clear all
yi = 0: 38.2: 38.2*2912;
xi = 0: 38.2: 38.2*2774;

%doc  plot %scatter%xlsread
z = xlsread('C:\Users\mengw\Desktop\2017-数学建模大赛\2017年试题\A\附件1 区域高程数据.xlsx');
z=z';
%surf(x, y, z)

AreaTm=0;
for m=1:1:2775
    for n=1:1:2913
       if z(n,m)<3000
          AreaTm=AreaTm+38.2*38.2*(((n-1)*38.2-110000)^2+((m-1)*38.2)^2)^(1/2);  
       end 
    end
end 
AreaTm

AreaTm2=0;
for n=1:1:2775
    for m=1:1:2913
       if z(m,n)<3000
          AreaTm2=AreaTm2+38.2*38.2*(((m-1)*38.2-110000)^2+((n-1)*38.2-55000)^2)^(1/2);  
       end 
    end
end 
AreaTm2



