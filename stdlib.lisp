(define (getlistelem x n)
  (if (= n 0) (car x) (getlistelem (cdr x) (- n 1))))

(define (gettupleelem x n)
  (if (= n 0) (car x)
    (if (= n 1) 
      (if (atom? (cdr x)) (cdr x)
        (gettupleelem (cdr x) (- n 1)))
      (gettupleelem (cdr x) (- n 1)))))
