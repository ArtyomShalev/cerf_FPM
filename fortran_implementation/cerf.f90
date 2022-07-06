program main
    use faddeeva_fortran_interface, only: Faddeeva_w
    use cerf_lib
    complex(dp), allocatable :: res_fortran(:), res_MIT(:), ref(:), res(:)
    real(dp), allocatable :: rp_fortran(:), ip_fortran(:), rp_MIT(:), ip_MIT(:), ref_rp(:), ref_ip(:), &
                             re_err(:), im_err(:)
    integer :: i, num_args
    real :: start, finish,  sum
    character (len=10) :: exp_fmt
    include 'reference_data.f90'
    !=======================================================================
    num_args = size(Faddeeva_w_args)
    allocate(res_fortran(1:num_args))
    allocate(res_MIT(1:num_args))
    allocate(rp_fortran(1:num_args))
    allocate(ip_fortran(1:num_args))
    allocate(rp_MIT(1:num_args))
    allocate(ip_MIT(1:num_args))
    allocate(ref(1:num_args))
    allocate(ref_rp(1:num_args))
    allocate(ref_ip(1:num_args))
    allocate(res(1:num_args))
    allocate(re_err(1:num_args))
    allocate(im_err(1:num_args))
    sum_fortran = 0
    sum_MIT = 0
    do i = 1, num_args
        do j = 1, 10000
            !---- Faddeeva MIT -------
            call cpu_time(start)
            res(i) = Faddeeva_w(Faddeeva_w_args(i), 0.0_dp)
            call cpu_time(finish)
            sum_MIT = sum_MIT + (finish-start)
            rp_MIT(i) = real(res(i))
            ip_MIT(i) = aimag(res(i))
            ! ----- References SG Johnson -----------
            ref(i) = Faddeeva_w_wolfram_refs(i)
            ref_rp(i) = real(ref(i))
            ref_ip(i) = aimag(ref(i))
            ! ----- Faddeeva fortran imp from Matlab
            call cpu_time(start)
            res_fortran(i) = cerf(Faddeeva_w_args(i))
            call cpu_time(finish)
            sum_fortran = sum_fortran + (finish-start)
!            print *, i, j,  'sum_fortran', sum_fortran
            rp_fortran(i) = real(res_fortran(i))
            ip_fortran(i) = aimag(res_fortran(i))
        end do
    end do

    print *, 'sum_fortran', sum_fortran
    print *, 'sum_MIT', sum_MIT

    open(unit=20, file='../data/fortran_rp.txt')
    open(unit=30, file='../data/fortran_ip.txt')
    open(unit=40, file='../data/MIT_rp.txt')
    open(unit=50, file='../data/MIT_ip.txt')
    open(unit=60, file='../data/ref_rp.txt')
    open(unit=70, file='../data/ref_ip.txt')

    exp_fmt = "(e25.16e3)"

    do i = 1, num_args
        write(unit=20,fmt=exp_fmt) rp_fortran(i)
        write(unit=30,fmt=exp_fmt) ip_fortran(i)
        write(unit=40,fmt=exp_fmt) rp_MIT(i)
        write(unit=50,fmt=exp_fmt) ip_MIT(i)
        write(unit=60,fmt=exp_fmt) ref_rp(i)
        write(unit=70,fmt=exp_fmt) ref_ip(i)
    end do

    close(unit=20)
    close(unit=30)
    close(unit=40)
    close(unit=50)
    close(unit=60)
    close(unit=70)

end program main