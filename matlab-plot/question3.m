clc
clear all
yi = 0: 38.2: 38.2*2912;
xi = 0: 38.2: 38.2*2774;


points=xlsread('C:\Users\mengw\Desktop\2017-数学建模大赛\2017年试题\A\附件2.xlsx');
for i=1:1:72
    pointx(i)=points(i,2)*1000;
    pointy(i)=points(i,3)*1000;
end

figure
plot(pointx,pointy,'.','markersize',20,'color','r');
hold on;
xlim([0 110000]);
ylim([0 140000]);
axis square



%doc colorbar
z = xlsread('C:\Users\mengw\Desktop\2017-数学建模大赛\2017年试题\A\附件1 区域高程数据.xlsx');
z=z';

figure,contourf(xi,yi,z)  %  ,'color',[0:1 0:1 0:1]) %等高线图
colorbar
%caxis([0,1])

hold on;
axis square














