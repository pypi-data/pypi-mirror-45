import re,math

__all__ = ['normalize']

def vectorAngle(v1,v2):
    sign = -1 if (v1[0] * v2[1] - v1[1] * v2[0] < 0) else 1
    dot = v1[0] * v2[0] + v1[1] * v2[1]
    # Add this to work with arbitrary vectors:
    # dot /= (math.sqrt(v1[0] * v1[0] + v1[1] * v1[1]) * math.sqrt(v2[0] * v2[0] + v2[1] * v2[1]))
    dot = max(-1.0,min(dot,10))
    return sign * math.acos(dot)

def cubicArc(x1, y1, x2, y2, rx, ry, fa, fs, theta):
    sin = math.sin(theta * math.pi / 180)
    cos = math.cos(theta * math.pi / 180)

    # Step 1.
    # Moving an ellipse so origin will be the middlepoint between our two points. After that, rotate it to line up ellipse axes with coordinate axes.
    x1p =  cos * (x1-x2)/2 + sin * (y1-y2)/2
    y1p = -sin * (x1-x2)/2 + cos * (y1-y2)/2

    if (x1p == 0 and y1p == 0):
        # we're asked to draw line to itself
        return []

    # Make sure radii are valid
    if (rx == 0 or ry == 0):
        # one of the radii is zero
        return []
    # Compensate out-of-range radii
    rx = abs(rx)
    ry = abs(ry)
    LAMBDA = (x1p * x1p) / (rx * rx) + (y1p * y1p) / (ry * ry)
    if LAMBDA > 1:
        rx *= math.sqrt(LAMBDA)
        ry *= math.sqrt(LAMBDA)

    # Step 2 - Compute coordinates of the center of this ellipse (cx', cy') in the new coordinate system.
    radicant = (rx*rx*ry*ry - rx*rx*y1p*y1p - ry*ry*x1p*x1p)
    if (radicant < 0): radicant = 0

    rcoeff = (-1 if fa==fs else 1) * math.sqrt(radicant / (rx*rx*y1p*y1p + ry*ry*x1p*x1p))

    cxp = (rx*y1p)/ry * rcoeff
    cyp = -(ry*x1p)/rx * rcoeff

    # Step 3 - Transform back to get centre coordinates (cx, cy) in the original coordinate system.
    cx = cos * cxp - sin * cyp + (x1+x2)/2
    cy = sin * cxp + cos * cyp + (y1+y2)/2

    # Step 4 - Compute angles (theta1, delta_theta).
    v1 = [(x1p-cxp)/rx,(y1p-cyp)/ry]
    v2 = [(-x1p-cxp)/rx,(-y1p-cyp)/ry]
    angle1 = vectorAngle([1,0], v1)
    delta = vectorAngle(v1,v2)
    if fs == 0 and delta > 0:
        delta -= 2 * math.pi
    if fs == 1 and delta < 0:
        delta += 2 * math.pi

    result = []

    # Split an arc to multiple segments, so each segment will be less than τ/4 (= 90°)
    segments = max(math.ceil(abs(delta) / (math.pi / 2)), 1)

    delta /= segments
    alpha = 4/3 * math.tan(delta/4)
    for i in range(0,segments):
        # Approximate Unit Arc
        ax1,ay1 = math.cos(angle1),math.sin(angle1)
        ax2,ay2 = math.cos(angle1 + delta),math.sin(angle1 + delta)
        result.append([(ax1,ay1),(ax1 - ay1*alpha, ay1 + ax1*alpha),(ax2 + ay2*alpha, ay2 - ax2*alpha),(ax2, ay2)])
        angle1 += delta
    # We have a bezier approximation of a unit circle, now need to transform back to the original ellipse

    transform = lambda x,y : (cos*x*rx - sin*y*ry + cx,sin*x*rx + cos*y*ry + cy)
    return [[transform(x,y) for (x,y) in curve] for curve in result]


def normalize(path,*dim):
    if len(dim) == 1 and type(dim[0])==str:
        dim = tuple(int(x) for x in re.split(r'[ ,]+',dim[0].strip()))
    if len(dim) == 1:
        w,h = (*dim,*dim)
    elif len(dim) == 2:
        w,h = dim
    else:
        w,h = dim[-2:]
    current = (0.0,0.0)

    def normalize_point(x,y):
        if type(x) == str: x = float(x)
        if type(y) == str: y = float(y)
        return "{0:.6f} {1:.6f}".format(x/w,y/h)

    def normalize_seg(svg):
        nonlocal current
        cmd,data = svg[0],re.findall(r'-?[\d.]+',svg[1:].strip())
        if cmd.lower() == 'a':
            # [rx] [ry] [x-axis-rotation] [large-arc-flag] [sweep-flag] [x] [y]
            rx,ry = (float(x) for x in data[:2])
            x2,y2 = (float(x) for x in data[5:])
            x1,y1 = current
            theta,fa,fs = float(data[2]),int(data[3]),int(data[4])
            if cmd.islower():
                x2,y2 = x1+x2,y1+y2
            current = (x2,y2)
            curves = cubicArc(x1,y1,x2,y2,rx,ry, fa, fs, theta)
            if len(curves) == 0:
                return "L%s"%normalize_point(x2,y2)
            return " ".join("C%s"%" ".join(normalize_point(*p) for p in curve[1:]) for curve in curves)

        floats = [float(f) for f in data]
        if len(floats) == 1:
            if cmd.lower() == "v":
                points = [(current[0],(floats[0]+current[1]) if cmd.islower() else floats[0])]
                cmd = "L"
            elif cmd.lower() == "h":
                points = [((floats[0]+current[0]) if cmd.islower() else floats[0],current[1])]
                cmd = "L"
            else:
                raise "Illegal Segment -> {} {}".format(cmd,data)
        else:
            points = [*zip(floats[0::2],floats[1::2])]
            if cmd.islower():
                points = [(x+current[0],y+current[1]) for (x,y) in points]

        current = points[-1]
        return cmd.upper() + ' '.join(normalize_point(*p) for p in points)

    def normalize_subpath(spath):
        nonlocal current
        closed = False
        if spath[-1].lower()=='z':
            closed = True
            spath = spath[:-1]
        segments = re.findall(r'[A-Za-z][ \-,0-9.]+',spath)
        normalized = [normalize_seg(segments[0])]
        startPoint = current
        normalized = normalized + [normalize_seg(x) for x in segments[1:]]
        code = " ".join(normalized)+" "
        if closed:
            code += "z"
            current = startPoint
        return re.sub(r'(\.(?:0|[1-9]+))0+(?= )',r'\1',code)

    return ' '.join(normalize_subpath(x) for x in re.findall(r'[^zZ]+[zZ]?',path.strip()))
