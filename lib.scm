(begin
  
  (define #t 1)
  (define #f 0)
  (define nil (quote ()))
  
  (define null? (lambda (lst) (if (eq? lst nil) #t #f)))

  (define map
    (lambda (fn lst)
      (if (null? lst)
        lst
        (cons (fn (car lst)) (map fn (cdr lst))))))

  (define not (lambda (a)   (if a #f #t)))
  (define or  (lambda (a b) (if a #t  b)))
  (define and (lambda (a b) (if a  b #f)))
  (define xor (lambda (a b) (or (and (not a) b) (and a (not b)))))

  (define neg (lambda (n) (- 0 x)))
  (define abs (lambda (n) (if (<= n 0) (neg n) n)))
  (define !   (lambda (n) (if (= n 1) 1 (* n (! (- n 1))))))

)
