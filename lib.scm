(begin
  
  (define #t 1)
  (define #f 0)
  
  (define neg (lambda (x) (- 0 x)))
  (define abs (lambda (x) (if (<= x 0) (neg x) x)))
  (define !   (lambda (x) (if (= x 1) 1 (* x (! (- x 1))))))

)
