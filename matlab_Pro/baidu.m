function [direct_N(1,4),leng_direct]=baidu([Nx,Ny],sarea_func(87,91))
    direct_N=zeros(1,4);
    value_max=max{sarea_func(Nx-1,Ny),sarea_func(Nx,Ny-1),sarea_func(Nx+1,Ny),sarea_func(Nx,Ny+1)};  %1×ó£¬2ÏÂ£¬3ÓÒ£¬4ÉÏ
    if  length(find([sarea_func(Nx-1,Ny),sarea_func(Nx,Ny-1),sarea_func(Nx+1,Ny),sarea_func(Nx,Ny+1)]==value_max))>1
            leng_direct=length(find([sarea_func(Nx-1,Ny),sarea_func(Nx,Ny-1),sarea_func(Nx+1,Ny),sarea_func(Nx,Ny+1)]==value_max));
            temp_arry(1,leng_direct)=find([sarea_func(Nx-1,Ny),sarea_func(Nx,Ny-1),sarea_func(Nx+1,Ny),sarea_func(Nx,Ny+1)]==value_max;
      for i=1:1:leng_direct
            direct_N(1,i)=temp_arry(1,i);    
      end
    end
end