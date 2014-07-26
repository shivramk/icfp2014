(define (getlistelem x n)
  (if (= n 0) (car x) (getlistelem (cdr x) (- n 1))))

(define (square x) (* x x))

(define (get-square) square)

(define (main)
  ((get-square) 20))
