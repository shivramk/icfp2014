(define (incrementer x)
  (define (inc v)
    (+ x v))
  inc)

(define (main) ((incrementer 20) 5))
