(define (main) (testit 5))

(define (testit x)
  (set! b 10)
  (define (meow y z)
    (+ x (+ y z)))
  (define (helloworld meow c b)
    (set! b 18)
    (if (= c 0) (meow b 5) (helloworld meow (- c 1) b)))
  (helloworld meow 3 b)
  (debug b))