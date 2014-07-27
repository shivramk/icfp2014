(define (main) (testit 5))

(define (foobar func x)
  (set! y 20)
  (debug (func y 10)))

(define (testit x)
  (define (meow y z)
    (+ x (+ y z)))
  (if 1 (foobar meow)))
