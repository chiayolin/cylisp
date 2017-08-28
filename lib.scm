(begin

  (define else #t)
  (define nil  (' ()))

  (define if    (lambda (p e a) (cond (p e) (else a))))
  (define null? (lambda (lst) (eq? lst nil)))
  (define apply (lambda (f x) (f x)))

  (define not (lambda (a)   (if a #f #t)))
  (define or  (lambda (a b) (if a #t  b)))
  (define and (lambda (a b) (if a  b #f)))
  (define xor (lambda (a b) (or (and (not a) b) (and a (not b)))))

  (define ++  (lambda (n)   (+ n 1)))
  (define --  (lambda (n)   (- n 1)))
  (define neg (lambda (n)   (- 0 n)))
  (define mod (lambda (x y) (- x (* (// x y) y))))

  (define negative? (lambda (n) (< n 0)))
  (define zero?     (lambda (n) (= n 0)))
  (define positive? (lambda (n) (> n 0)))
  (define even?     (lambda (n) (= (mod n 2) 0)))
  (define odd?      (lambda (n) (not (even? n))))

  (define abs (lambda (n)   (if (<= n 0) (neg n) n)))
  (define pow (lambda (b e) (if (= e 1) b (* b (pow b (-- e))))))
  (define !   (lambda (n)   (if (= n 1) 1 (* n (! (-- n))))))
  
  (define caar   (lambda (x) (car (car x))))
  (define cadr   (lambda (x) (car (cdr x))))
  (define cdar   (lambda (x) (cdr (car x))))
  (define cddr   (lambda (x) (cdr (cdr x))))
  (define caaar  (lambda (x) (car (car (car x)))))
  (define caadr  (lambda (x) (car (car (cdr x)))))
  (define cadar  (lambda (x) (car (cdr (car x)))))
  (define caddr  (lambda (x) (car (cdr (cdr x)))))
  (define cdaar  (lambda (x) (cdr (car (car x)))))
  (define cdadr  (lambda (x) (cdr (car (cdr x)))))
  (define cddar  (lambda (x) (cdr (cdr (car x)))))
  (define cdddr  (lambda (x) (cdr (cdr (cdr x)))))
  (define caaaar (lambda (x) (car (car (car (car x))))))
  (define caaadr (lambda (x) (car (car (car (cdr x))))))
  (define caadar (lambda (x) (car (car (cdr (car x))))))
  (define caaddr (lambda (x) (car (car (cdr (cdr x))))))
  (define cadaar (lambda (x) (car (cdr (car (car x))))))
  (define cadadr (lambda (x) (car (cdr (car (cdr x))))))
  (define caddar (lambda (x) (car (cdr (cdr (car x))))))
  (define cadddr (lambda (x) (car (cdr (cdr (cdr x))))))
  (define cdaaar (lambda (x) (cdr (car (car (car x))))))
  (define cdaadr (lambda (x) (cdr (car (car (cdr x))))))
  (define cdadar (lambda (x) (cdr (car (cdr (car x))))))
  (define cdaddr (lambda (x) (cdr (car (cdr (cdr x))))))
  (define cddaar (lambda (x) (cdr (cdr (car (car x))))))
  (define cddadr (lambda (x) (cdr (cdr (car (cdr x))))))
  (define cdddar (lambda (x) (cdr (cdr (cdr (car x))))))
  (define cddddr (lambda (x) (cdr (cdr (cdr (cdr x))))))

  (define list 
    (lambda (x y) (cons x (cons y (' ())))))
  
  (define append
    (lambda (x y)
      (if (null? x) y
        (cons (car x) (append (cdr x) y)))))

  (define pair
    (lambda (x y)
      (cond ((and (null? x) (null? y)) (' ()))
            ((and (not (atom? x)) (not (atom? y)))
             (cons (list (car x) (car y))
                   (pair (cdr x) (cdr y)))))))

  (define assoc
    (lambda (x y)
      (if (eq? (caar y) x) (cadar y)
        (assoc x (cdr y)))))

  (define map
    (lambda (fn lst)
      (if (null? lst) lst
        (cons (fn (car lst)) (map fn (cdr lst))))))

  (define range
    (lambda (a b)
      (if (= a b) (quote ()) (cons a (range (++ a) b)))))
  
  (define eval 
    (lambda (e a)
      (cond
        ((atom? e) (assoc e a))
        ((atom? (car e))
         (cond
           ((eq? (car e) (' quote)) (cadr e))
           ((eq? (car e) (' atom?)) (atom?  (eval (cadr e) a)))
           ((eq? (car e) (' eq?))   (eq?    (eval (cadr e) a)
                                            (eval (caddr e) a)))
           ((eq? (car e) (' car))   (car    (eval (cadr e) a)))
           ((eq? (car e) (' cdr))   (cdr    (eval (cadr e) a)))
           ((eq? (car e) (' cons))  (cons   (eval (cadr e) a)
                                            (eval (caddr e) a)))
           ((eq? (car e) (' cond))  (evcon  (cdr e) a))
           (else (eval (cons (assoc (car e) a)
                              (cdr e))
                       a))))
        ((eq? (caar e) (' label))
         (eval (cons (caddar e) (cdr e))
               (cons (list (cadar e) (car e)) a)))
        ((eq? (caar e) (' lambda))
         (eval (caddar e)
               (append (pair (cadar e) (evlis (cdr e) a))
                       a))))))
  
    (define evcon 
      (lambda (c a)
        (cond ((eval (caar c) a)
               (eval (cadar c) a))
              (else (evcon (cdr c) a)))))

    (define evlis 
      (lambda (m a)
        (cond ((null? m) (' ()))
              (else (cons (eval  (car m) a)
                          (evlis (cdr m) a))))))

)
