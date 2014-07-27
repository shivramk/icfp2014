(define (at map ghostlocs x y)
  (set! row (getlistelem map y))
  (if (contains? ghostlocs (cons x y) cmploc) 6
      (getlistelem row x)))

(define (contains? list elem cmp)
  (if (atom? list) 0
    (if (cmp elem (car list)) 1
      (contains? (cdr list) elem cmp))))

(define (cmploc l1 l2)
  (and (= (car l1) (car l2)) (= (cdr l1) (cdr l2))))

(define (min a b)
  (if (< a b) a b))

(define (max a b)
  (if (> a b) a b))

(define (min4 a b c d)
  (min a (min b (min c d))))

(define (max4 a b c d)
  (max a (max b (max c d))))

(define (maxidx1 list curidx maxidx maxval)
  (if (atom? list) maxidx
    (if (> (car list) maxval)
      (maxidx1 (cdr list) (+ curidx 1) curidx (car list))
      (maxidx1 (cdr list) (+ curidx 1) maxidx maxval))))

(define (minidx1 list curidx minidx minval)
  (if (atom? list) minidx
    (if (< (car list) minval)
      (minidx1 (cdr list) (+ curidx 1) curidx (car list))
      (minidx1 (cdr list) (+ curidx 1) minidx minval))))

(define (maxidx l)
  (maxidx1 (cdr l) 1 0 (car l)))

(define (minidx l)
  (minidx1 (cdr l) 1 0 (car l)))

(define (item-score v)
  (if (= v 0) -1000000
    (if (= v 1) 1
      (if (= v 2) 10
        (if (= v 3) 50
          (if (= v 4) 100
            (if (= v 5) 1 -1000)))))))

(define (score width height map ghostlocs x y s depth)
  (if (or (or (< x 0) (>= x width)) (or (< y 0) (>= y height))) s
    (if (<= depth 0) s
      (if (< s -100000) s
          (best-score width height map ghostlocs x y s (- depth 1)
                      (item-score (at map ghostlocs x y)))))))

(define (best-score width height map ghostlocs x y s depth v)
  (set! left  (score width height map ghostlocs (- x 1) y (+ s v) depth))
  (set! right (score width height map ghostlocs (+ x 1) y (+ s v) depth))
  (set! up    (score width height map ghostlocs x (- y 1) (+ s v) depth))
  (set! down  (score width height map ghostlocs x (+ y 1) (+ s v) depth))
  (set! minscore (min4 left right up down))
  (set! maxscore (max4 left right up down))
  (if 0 minscore maxscore))

(define (findpill map ghostlocs x y dir step width height dist)
  (if (or (or (< x 0) (>= x width)) (or (< y 0) (>= y height))) (- 10000 dist)
    (do (set! val (at map ghostlocs x y))
      (if (or (= val 2) (or (= val 3) (= val 4))) dist
        (if (= val 1)
          (if (= dir 0)
            (findpill map ghostlocs (+ x step) y dir step width height (+ dist 1))
            (findpill map ghostlocs x (+ y step) dir step width height (+ dist 1))) 
          (- 10000 dist))))))

(define (penalty s d oppd)
  (if (= d oppd)
    (- s 30) s))

(define (mod x y)
  (- x (* (/ x y) y)))

(define (map list func)
  (if (atom? list) list
    (cons (func (car list)) (map (cdr list) func))))

(define (getloc x) (getlistelem x 1))

(define (make_move worldstate)
  (set! worldmap (gettupleelem worldstate 0))
  (set! lambdastate (gettupleelem worldstate 1))
  (set! height (len worldmap))
  (set! width (len (getlistelem worldmap 0)))
  (set! lpos (gettupleelem lambdastate 1))
  (set! x (gettupleelem lpos 0))
  (set! y (gettupleelem lpos 1))
  (set! dir (gettupleelem lambdastate 2))
  (set! ghoststate (gettupleelem worldstate 2))
  (set! ghostlocs (map ghoststate getloc))
  (set! oppdir (mod (+ 2 dir) 4))
  (set! depth 4)
  (set! sleft  (penalty (score width height worldmap ghostlocs (- x 1) y 0 depth) 3 oppdir))
  (set! sright (penalty (score width height worldmap ghostlocs (+ x 1) y 0 depth) 1 oppdir))
  (set! sup    (penalty (score width height worldmap ghostlocs x (- y 1) 0 depth) 0 oppdir))
  (set! sdown  (penalty (score width height worldmap ghostlocs x (+ y 1) 0 depth) 2 oppdir))
  (set! maxscore (max4 sleft sright sup sdown))
  (debug maxscore)
  (if (= maxscore depth)
    (do 
      (set! sleft  (findpill worldmap ghostlocs x y 0 -1 width height 0))
      (set! sright (findpill worldmap ghostlocs x y 0  1 width height 0))
      (set! sup    (findpill worldmap ghostlocs x y 1 -1 width height 0))
      (set! sdown  (findpill worldmap ghostlocs x y 1  1 width height 0))
      (debug (cons sleft (cons sright (cons sup (cons sdown 0)))))
      (minidx (cons sup (cons sright (cons sdown (cons sleft 0))))))
    (maxidx (cons sup (cons sright (cons sdown (cons sleft 0)))))))

(define (step aistate worldstate) 
  (cons 0 (make_move worldstate)))

(define (main worldstate undocumented) 
  (cons 0 step))
