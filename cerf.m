function res = cerf(z)
%% Calculate the complex error function w(z) = exp(-z^2)*(1 - erf(-i*z))
% INPUT
%   z       Argument (complex)
% OUTPUT
%   res     Result

%% For z == 0 there's nothing to calculate
if z == 0
    res = 1;
    return
end

%% Translate to first quadrant
z_orig = z;
z = abs(real(z)) + abs(imag(z))*1i;

%% Depending on the value z choose a suitable approximation
if abs(z) > 10
    % See Abramowitz, Handbook of mathematical functions with formulas, graphs, and mathematical tables, 1965 (p. 328)
    res = 1i*z*(0.5124242/(z^2-0.2752551)+0.05176536/(z^2-2.724745));
elseif imag(z) < 1 && abs(z) < 4
    % See Abramowitz (p. 297)
    acc = z;
    for n = 1:500
        last = z^(2*n+1)/(factorial(n)*(2*n+1));
        acc = acc + last;
        if abs(last) < eps
            break
        end
    end
    res = exp(-z^2)*(1 + 2i*acc/sqrt(pi));
else
    old = 1e6;
    h1 = 1;
    h2 = 2*z;
    u1 = 0;
    u2 = 2*sqrt(pi);
    for n = 1:300
        h3 = h2*z - n*h1;
        u3 = u2*z - n*u1;
        h1 = h2;
        h2 = 2*h3;
        u1 = u2;
        u2 = 2*u3;
        new = u3/h3;
        if abs((new-old)/old) < 5e-6
            break
        elseif ~isfinite(new) 
            new = old;
            break;
        end
        old = new;
    end
    res = 1i*new/pi;
end

%% Translate the result to the original quadrant
if real(z_orig) < 0
    if imag(z_orig) >=0
        res = conj(res);
    else
        res = 2*exp(-z^2) -res;
    end
elseif imag(z_orig) < 0
    res = conj(2*exp(-z^2) - res);
end
 