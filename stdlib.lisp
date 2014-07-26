(define (getlistelem x n)
  (if (= n 0) (car x) (getlistelem (cdr x) (- n 1))))

(define (gettupleelem x n)
  (if (= n 0) (car x)
    (if (= n 1) 
      (if (atom? (cdr x)) (cdr x)
        (gettupleelem (cdr x) (- n 1)))
      (gettupleelem (cdr x) (- n 1)))))

(define (len x) (length1 x 0))

(define (length1 x l)
  (if (atom? x) l
    (length1 (cdr x) (+ l 1))))

(define (append x v)
  (if (atom? x) (cons v 0)
    (cons (car x) (append (cdr x) v))))
