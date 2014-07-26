(define (at map x y)
  (set! row (getlistelem map y))
  (getlistelem row x))

(define (max a b)
  (if (> a b) a b))

(define (max4 a b c d)
  (max a (max b (max c d))))

(define (maxidx1 list curidx maxidx maxval)
  (if (atom? list) maxidx
    (if (> (car list) maxval)
      (maxidx1 (cdr list) (+ curidx 1) curidx (car list))
      (maxidx1 (cdr list) (+ curidx 1) maxidx maxval))))

(define (maxidx l)
  (maxidx1 (cdr l) 1 0 (car l)))

(define (item-score v)
  (if (= v 0) -1000000
    (if (= v 1) 1
      (if (= v 2) 10
        (if (= v 3) 50
          (if (= v 4) 100
            (if (= v 5) -100 -1000)))))))

(define (score width height map x y s depth)
  (if (or (or (< x 0) (>= x width)) (or (< y 0) (>= y height))) 0
    (if (<= depth 0) s
      (if (< s -100000) s
          (best-score width height map x y s (- depth 1) (item-score (at map x y)))))))

(define (best-score width height map x y s depth v)
   (max4
     (score width height map (- x 1) y (+ s v) depth)
     (score width height map (+ x 1) y (+ s v) depth)
     (score width height map x (- y 1) (+ s v) depth)
     (score width height map x (+ y 1) (+ s v) depth)))

(define (make_move worldstate)
  (set! worldmap (gettupleelem worldstate 0))
  (set! lambdastate (gettupleelem worldstate 1))
  (set! height (len worldmap))
  (set! width (len (getlistelem worldmap 0)))
  (set! lpos (gettupleelem lambdastate 1))
  (set! x (gettupleelem lpos 0))
  (set! y (gettupleelem lpos 1))
  (set! sleft  (score width height worldmap (- x 1) y 0 3))
  (set! sright (score width height worldmap (+ x 1) y 0 3))
  (set! sup    (score width height worldmap x (- y 1) 0 3))
  (set! sdown  (score width height worldmap x (+ y 1) 0 3))
  (debug sleft)
  (debug sright)
  (debug sup)
  (debug sdown)
  (maxidx (cons sup (cons sright (cons sdown (cons sleft 0))))))

(define (step aistate worldstate) 
  (cons 0 (make_move worldstate)))

(define (main worldstate undocumented) 
  (cons 0 step))
