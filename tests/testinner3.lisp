(define (incrementer x)
  (set! y x)
  (define (inc)
    (set! y (+ y 1))
    y)
  inc)

(define (main) 
  (set! i (incrementer 20))
  (debug (i))
  (debug (i))
  (debug (i))
  (debug (i)))