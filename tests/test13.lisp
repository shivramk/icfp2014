(define (square x) (* x x))

(define (get-square) square)

(define (main)
  ((get-square) 20))
