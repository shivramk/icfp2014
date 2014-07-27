(define (main) (test3 5) (debug -1))

(define (test2 x)
  (cond ((= x 1) (debug 1))
        ((= x 2) (debug 2))
        ((= x 3) (debug 3))
        (else (debug 100000))))

(define (test3 x)
  (cond ((= x 1) (debug 1))
        ((= x 2) (debug 2))))

(define (test x)
  (set! y 1)
  (if (= x 5) 
    (set! y (+ y 1))
    (set! y (+ y 2)))
  y)
