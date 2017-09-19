clc
clear all
yi = 0: 38.2: 38.2*2912;
xi = 0: 38.2: 38.2*2774;


points=xlsread('C:\Users\mengw\Desktop\2017-��ѧ��ģ����\2017������\A\����2.xlsx');
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
z = xlsread('C:\Users\mengw\Desktop\2017-��ѧ��ģ����\2017������\A\����1 ����߳�����.xlsx');
z=z';

figure,contourf(xi,yi,z)  %  ,'color',[0:1 0:1 0:1]) %�ȸ���ͼ
colorbar
%caxis([0,1])

hold on;
axis square














