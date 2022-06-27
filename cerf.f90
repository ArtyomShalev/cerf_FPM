program main
    use cerf_lib
    complex(dp) :: z
    !=======================================================================
    z = cmplx(10.0_dp, 10.0_dp, dp)

    print *, cerf(z)

end program main