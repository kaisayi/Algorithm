clc 
clear all
yi = 0: 38.2: 38.2*2912;
xi = 0: 38.2: 38.2*2774;

%doc  plot %scatter%xlsread
z = xlsread('C:\Users\mengw\Desktop\2017-数学建模大赛\2017年试题\A\附件1 区域高程数据.xlsx');
z=z';
%surf(x, y, z)

for n=1:1:2775
    for m=1:1:2913
       if z(m,n)<3000
          z(m,n)=0;  
       end 
    end
end 
figure,contourf(xi,yi,z) %等高线图
colorbar
hold on;

xh1=110000;
yh1=0;
plot(xh1,yh1,'.','markersize',25);
hold on

xh2=110000;
yh2=55000;
plot(xh2,yh2,'.','markersize',25);
hold on

set(gca,'xtickmode','manual','ytickmode','manual','ztickmode','manual')
%figure,surfc(X,Y,Z)%三维曲面
%colorbar
%shading interp