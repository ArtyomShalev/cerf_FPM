program main
    use cerf_lib
    use faddeeva_fortran_interface, only: Faddeeva_w, find_relerr
    complex(dp), allocatable :: res(:)
    real(dp), allocatable :: rp(:), ip(:)
    integer :: i, num_args
    include 'reference_data.f90'
    !=======================================================================
    num_args = size(Faddeeva_w_args)
    allocate(res(1:num_args))
    allocate(rp(1:num_args))
    allocate(ip(1:num_args))
    do i = 1, num_args
        res(i) = cerf(Faddeeva_w_args(i))
        rp(i) = real(res(i))
        ip(i) = aimag(res(i))
    end do

    open(unit=20, file='fortran_rp.txt')
    open(unit=30, file='fortran_ip.txt')
    do i = 1, num_args
        write(unit=20,fmt=*) rp(i)
        write(unit=30,fmt=*) ip(i)
    end do
    close(unit=20)
    close(unit=30)

end program main