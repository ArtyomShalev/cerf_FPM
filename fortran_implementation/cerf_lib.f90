module cerf_lib
    implicit none
    integer, parameter :: dp = kind(0.0D0)
    complex(dp), parameter :: ci = (0.0_dp, 1.0_dp)
    real(dp), parameter :: pi = 4.0_dp * ATAN(1.0_dp), eps =  2.22e-16_dp, inf = HUGE(1.0_dp)
contains
    !=======================================================================
    recursive function factorial(n) result (f)
        integer :: f, n
        if( n == 1 ) then
            f = 1
        else
            f = n * factorial(n - 1)
        end if
    end function factorial


    complex(dp) function cerf(z)
        complex(dp) :: z, z_orig, acc, last, u2, u3, h2, h3, new, old, h1, u1
        real :: n_gamma
        integer :: n
        !-----------------------------------------
        if (z == 0.0_dp) then
            cerf = 1.0_dp
            return
        end if

        z_orig = z
        z = cmplx(abs(real(z)), abs(aimag(z)), dp)

        if (abs(z) > 10) then
            cerf = ci*z*(0.5124242/(z**2-0.2752551) + 0.05176536/(z**2-2.724745))
        else
            if (aimag(z) < 1 .and. abs(z) < 4) then
                acc = z
                do n = 1, 500
                    last = z**(2*n+1)/(factorial(n)*(2*n+1))
!                    n_gamma = n
!                    last = z**(2*n+1)/(gamma(n_gamma+1)*(2*n+1))

                    acc = acc + last
                    if (abs(last) < eps) exit
                end do
                cerf = exp(-z*z)*(1 + 2*ci*acc/sqrt(pi))
            else
                old = cmplx(1.0e6_dp, 0.0_dp, dp)
                h1 = cmplx(1.0_dp, 0.0_dp, dp)
                h2 = 2.0_dp*z
                u1 = cmplx(0.0_dp, 0.0_dp, dp)
                u2 = 2.0_dp*sqrt(pi)
                do n = 1, 300
                    h3 = h2*z - n*h1
                    u3 = u2*z - n*u1
                    h1 = h2
                    h2 = 2.0_dp*h3
                    u1 = u2
                    u2 = 2.0_dp*u3
                    new = u3/h3
                    if (abs((new-old)/old) < 5e-6_dp) then
                        exit
                    else
                        if (new == inf) then
                            new = old
                            exit
                        end if
                    end if
                    old = new
                end do
                cerf = ci*new/pi
            end if
        end if

        if (real(z_orig) < 0) then
            if (aimag(z_orig) >= 0) then
                cerf = conjg(cerf)
            else
                cerf = 2*exp(-z*z) - cerf
            end if
        else
            if (aimag(z_orig) < 0) then
                cerf = conjg(2*exp(-z*z) - cerf)
            end if
         end if

        return

    end function cerf

end module cerf_lib


