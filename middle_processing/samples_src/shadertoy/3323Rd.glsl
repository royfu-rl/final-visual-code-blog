float map (vec3 p) {
    float d = abs(p.z-.1);
    vec2 W = p.xy*.5*R.y+.5*R;
    vec4 a = A(W);
    d = min(d,length(p - vec3(a.xy,0))-abs(a.z));
    return d;

}
vec3 normal (vec3 p) {
    vec2 e = vec2(1e-3,0);
    float m = map(p);
    return normalize(vec3(
        map(p+e.xyy)-m,
        map(p+e.yxy)-m,
        map(p+e.yyx)-m
    ));
}
Main {
    Q = vec4(1);
    vec3 p = vec3(0,0,-1);
    vec3 d = normalize(vec3(2.*(U-.5*R)/R.y,1));
    if (iMouse.z>0.) {
    
    p.xz *= ei(sin(iMouse.x/R.x*6.));
    d.xz *= ei(sin(iMouse.x/R.x*6.));
    p.yz *= ei(sin(iMouse.y/R.y*6.));
    d.yz *= ei(sin(iMouse.y/R.y*6.));
    } else {
    p.xz *= ei(sin(iTime));
    d.xz *= ei(sin(iTime));
    }
    for (float i = 0.; i < 200.; i++) {
        float m = map(p);
        if (m > 2.) break;
        p += .8*d*m;
        if (abs(m) < 1e-4) {
            vec3 n = normal(p);
            d = reflect(d,n);
            vec2 W = p.xy*.5*R.y+.5*R;
            vec4 a = A(W);
            if (length(p.xy-a.xy) - a.z < 0.) 
            Q = mix(Q,.5-.5*abs(sin(vec4(1,2,3,4)+1000.*a.y+a.x)),.5);
            p += 2e-3*d;
        }
        
    }
    Q *= .8+.5*texture(iChannel1,d);
}
