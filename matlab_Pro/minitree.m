clc
clear all
z = xlsread('C:\Users\mengw\Desktop\2017-数学建模大赛\PPT图片\最小生成树数据.xlsx');

figure
for i=1:1:71
    plot(z(i,1),z(i,2),'.','markersize',30,'color','r');
    hold on
    xlim([0,110]);
    ylim([0,140]);
    axis square
end
plot(z(1,3),z(1,4),'.','markersize',20,'color','r');

for  j=1:1:71
    line([z(j,1),z(j,3)],[z(j,2),z(j,4)],'color','g','linewidth',3);
    hold on
end

points= xlsread('C:\Users\mengw\Desktop\2017-数学建模大赛\PPT图片\半径元.xlsx');

for m=1:1:154
    r=6;
    theta=0:pi/50:2*pi;
    x=points(m,1)+r*cos(theta);
    y=points(m,2)+r*sin(theta);
    plot(x,y,'-',points(m,1),points(m,2),'.','markersize',2,'color','y','linewidth',2);
    axis([0 110  0 140]); 
    %scatter(x(i)*1000,y(i)*1000,10000,'filled')
    axis square;
    hold on
end 