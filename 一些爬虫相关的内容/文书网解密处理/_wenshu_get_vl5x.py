# 文书网 get_vl5x 纯python实现


import hashlib
import base64

def getvl5x(cookie):
    def b64(string):  return base64.b64encode(string.encode()).decode()
    def sha1(string): return hashlib.sha1(string.encode()).hexdigest()
    def md5(string):  return hashlib.md5(string.encode()).hexdigest()
    def strToLong(string):
        long = 0
        for idx,i in enumerate(string):
            long += ord(i) << idx%16
        return long
    def strToLongEn(string):
        long = 0
        for idx,i in enumerate(string):
            long += (ord(i) << idx%16) + idx
        return long
    def strToLongEn2(string, step):
        long = 0
        for idx,i in enumerate(string):
            long += (ord(i) << idx%16) + (idx * step)
        return long
    def strToLongEn3(string, step):
        long = 0
        for idx,i in enumerate(string):
            long += (ord(i) << idx%16) + (idx + step - ord(i))
        return long
    def mk0(string):
        x = string[5:30] + string[36:39]
        return md5(x)[4:28]
    def mk1(string):
        x = string[5:5+5*5] + '5' + string[1:3] + '1' + string[36:39]
        a = x[5:] + x[4:]
        b = x[12:] + a[-6:]
        c = x[4:] + a[6:]
        return md5(c)[4:28]
    def mk2(string):
        x = string[5:5+5*5] + '15' + string[1:3] + string[36:39]
        b = str(strToLong(x[5:])) + x[4:]
        c = x[4:] + b[5:]
        return md5(c)[1:25]
    def mk3(string):
        x = string[5:5+5*5] + '15' + string[1:3] + string[36:39]
        a = str(strToLongEn(x[5:])) + x[4:]
        b = x[4:] + a[5:]
        return md5(b)[3:27]
    def mk4(string):
        x = string[5:5+5*5] + '2' + string[1:3] + string[36:39]
        a = str(strToLongEn(x[5:])) + x[4:]
        b = md5(x[1:]) + str(strToLong(a[5:]))
        return md5(b)[3:27]
    def mk5(string):
        x = b64(string[5:5+5*5]+string[1:3]+'1') + string[36:39]
        return md5(x)[4:28]
    def mk6(string):
        x = string[5:30] + string[36:39]
        a = b64(x[4:14]) + x[2:]
        b = x[6:] + a[2:]
        return md5(b)[2:26]
    def mk7(string):
        x = b64(string[5:25] + '55' + string[1:3]) + string[36:39]
        a = str(strToLong(x[5:])) + x[4:]
        b = md5(x[1:]) + str(strToLong(a[5:]))
        return md5(b)[3:27]
    def mk8(string):
        x = b64(string[5:5+5*5-1] + '5-5') + string[1:3] + string[36:39]
        # aa = str(strToLong(x[1:])) + x[4:]
        a = str(strToLong(x[5:])) + x[4:]
        b = md5(x[1:]) + str(strToLongEn(a[5:]))
        return md5(b)[4:28]
    def mk9(string):
        x = string[5:5+5*5] + '5' + string[1:3] + '1' + string[36:39]
        a = x[5:] + x[4:]
        c = sha1(x[4:]) + a[6:]
        return md5(c)[4:28]
    def mk10(string):
        x = b64(string[5:5+5*5-1] + '5') + string[1:3] + string[36:39]
        a = str(strToLong(x[5:])) + x[4:]
        b = md5(x[1:]) + sha1(a[5:])
        return md5(b)[4:28]
    def mk11(string):
        x = string[5:5+5*5-1] + '2' + string[1:3] + string[36:39]
        a = str(strToLong(x[5:])) + x[2:]
        b = x[1:] + sha1(a[5:])
        return md5(b)[2:26]
    def mk12(string):
        x = string[5:5+5*5-1] + string[36:39] + '2' + string[1:3]
        a = str(strToLong(x[5:])) + x[2:]
        b = x[1:] + sha1(x[5:])
        return md5(b)[1:25]
    def mk13(string):
        x = string[5:5+5*5-1] + '2' + string[1:3]
        a = str(strToLong(x[5:])) + x[2:]
        b = b64(x[1:] + sha1(x[5:]))
        return md5(b)[1:25]
    def mk14(string):
        x = string[5:5+5*5-1] + '2' + string[1:3]
        a = str(strToLong(x[5:])) + x[2:]
        b = b64(x[1:] + x[5:] + x[1:4])
        return sha1(b)[1:25]
    def mk15(string):
        x = string[5:5+5*5-1] + '2' + string[1:3]
        a = str(strToLong(x[5:])) + x[2:]
        b = b64(a[1:] + x[5:] + x[2:5])
        return sha1(b)[1:25]
    def mk16(string):
        x = string[5:5+5*5-1] + '2' + string[1:3] + '-5'
        a = str(strToLongEn(x[5:])) + x[2:]
        b = b64(a[1:]) + str(strToLongEn2(x[5:],5)) + x[2:5]
        return md5(b)[2:26]
    def mk17(string):
        x = string[5:5+5*5-1] + '7' + string[1:3] + '-5'
        a = str(strToLongEn(x[5:])) + x[2:]
        b = b64(a[1:]) + str(strToLongEn2(x[5:],6)) + x[7:10]
        return md5(b)[:24]
    def mk18(string):
        x = string[5:5+5*5-1] + '7' + string[1:3] + '5' + string[7:10]
        a = str(strToLongEn(x[5:])) + x[2:]
        b = a[1:] + str(strToLongEn2(x[5:],6)) + x[7:10]
        return md5(b)[:24]
    def mk19(string):
        x = string[5:5+5*5-1] + '7' + string[5:7] + '5' + string[7:10]
        a = str(strToLongEn(x[5:])) + x[2:]
        b = a[1:] + str(strToLongEn3(x[5:],4)) + x[7:10]
        return md5(b)[:24]
    e = {
        0:mk0, 1:mk1, 2:mk2, 3:mk3, 4:mk4, 5:mk5, 6:mk6, 7:mk7, 8:mk8, 9:mk9, 10:mk10, 
        11:mk11, 12:mk12, 13:mk13, 14:mk14, 15:mk15, 16:mk16, 17:mk17, 18:mk18, 19:mk19, 
    }
    d = {
        20:[(mk10, mk5),1,25],   21:[(mk11, mk3),2,26],   22:[(mk14, mk19),3,27],  23:[(mk15, mk0),4,28],   24:[(mk16, mk1),1,25],   25:[(mk9, mk4),2,26],    
        26:[(mk10, mk5),3,27],   27:[(mk17, mk3),4,28],   28:[(mk18, mk7),1,25],   29:[(mk19, mk3),2,26],   30:[(mk0, mk7),3,27],    31:[(mk1, mk8),4,28],    
        32:[(mk4, mk14),3,27],   33:[(mk5, mk15),4,28],   34:[(mk3, mk16),1,25],   35:[(mk7, mk9),2,26],    36:[(mk8, mk10),3,27],   37:[(mk6, mk17),1,25],   
        38:[(mk12, mk18),2,26],  39:[(mk14, mk19),3,27],  40:[(mk15, mk0),4,28],   41:[(mk16, mk1),3,27],   42:[(mk9, mk4),4,28],    43:[(mk10, mk5),1,25],   
        44:[(mk17, mk3),2,26],   45:[(mk18, mk7),3,27],   46:[(mk19, mk17),4,28],  47:[(mk0, mk18),1,25],   48:[(mk1, mk19),2,26],   49:[(mk4, mk0),3,27],    
        50:[(mk5, mk1),4,28],    51:[(mk3, mk4),1,25],    52:[(mk7, mk14),2,26],   53:[(mk12, mk15),3,27],  54:[(mk14, mk16),4,28],  55:[(mk15, mk9),3,27],   
        56:[(mk16, mk10),4,28],  57:[(mk9, mk17),1,25],   58:[(mk10, mk18),2,26],  59:[(mk17, mk19),3,27],  60:[(mk18, mk0),1,25],   61:[(mk19, mk1),2,26],   
        62:[(mk0, mk4),3,27],    63:[(mk1, mk19),4,28],   64:[(mk4, mk0),3,27],    65:[(mk14, mk1),1,25],   66:[(mk15, mk4),2,26],   67:[(mk16, mk5),3,27],   
        68:[(mk9, mk3),4,28],    69:[(mk10, mk7),1,25],   70:[(mk17, mk0),2,26],   71:[(mk18, mk1),3,27],   72:[(mk19, mk4),4,28],   73:[(mk0, mk17),1,25],   
        74:[(mk1, mk18),2,26],   75:[(mk14, mk19),3,27],  76:[(mk15, mk0),4,28],   77:[(mk16, mk1),3,27],   78:[(mk9, mk4),4,28],    79:[(mk10, mk9),1,25],   
        80:[(mk17, mk10),2,26],  81:[(mk18, mk17),3,27],  82:[(mk14, mk18),1,25],  83:[(mk15, mk19),4,28],  84:[(mk16, mk0),1,25],   85:[(mk9, mk1),2,26],    
        86:[(mk10, mk4),3,27],   87:[(mk14, mk14),4,28],  88:[(mk15, mk15),1,25],  89:[(mk16, mk16),2,26],  90:[(mk9, mk9),3,27],    91:[(mk10, mk10),4,28],  
        92:[(mk17, mk17),3,27],  93:[(mk18, mk18),4,28],  94:[(mk19, mk19),1,25],  95:[(mk0, mk0),2,26],    96:[(mk1, mk1),3,27],    97:[(mk4, mk4),4,28],    
        98:[(mk5, mk5),3,27],    99:[(mk3, mk3),4,28],    100:[(mk7, mk3),1,25],   101:[(mk10, mk7),2,26],  102:[(mk17, mk18),1,25], 103:[(mk18, mk19),2,26], 
        104:[(mk19, mk0),3,27],  105:[(mk0, mk0),4,28],   106:[(mk1, mk1),1,25],   107:[(mk14, mk14),2,26], 108:[(mk15, mk15),3,27], 109:[(mk16, mk16),4,28], 
        110:[(mk9, mk9),1,25],   111:[(mk10, mk10),2,26], 112:[(mk17, mk17),3,27], 113:[(mk18, mk18),4,28], 114:[(mk19, mk19),3,27], 115:[(mk0, mk0),4,28],   
        116:[(mk1, mk1),1,25],   117:[(mk4, mk4),2,26],   118:[(mk5, mk15),3,27],  119:[(mk3, mk16),1,25],  120:[(mk19, mk9),1,25],  121:[(mk0, mk10),2,26],  
        122:[(mk1, mk17),3,27],  123:[(mk4, mk18),4,28],  124:[(mk5, mk19),1,25],  125:[(mk3, mk0),2,26],   126:[(mk7, mk1),3,27],   127:[(mk3, mk4),4,28],   
        128:[(mk7, mk5),1,25],   129:[(mk8, mk3),2,26],   130:[(mk14, mk7),3,27],  131:[(mk15, mk10),4,28], 132:[(mk16, mk17),3,27], 133:[(mk9, mk18),4,28],  
        134:[(mk10, mk19),1,25], 135:[(mk17, mk0),2,26],  136:[(mk18, mk1),1,25],  137:[(mk19, mk14),2,26], 138:[(mk0, mk15),3,27],  139:[(mk1, mk16),4,28],  
        140:[(mk4, mk9),1,25],   141:[(mk5, mk10),2,26],  142:[(mk3, mk17),3,27],  143:[(mk7, mk18),4,28],  144:[(mk17, mk19),1,25], 145:[(mk18, mk0),2,26],  
        146:[(mk19, mk1),3,27],  147:[(mk0, mk4),4,28],   148:[(mk1, mk5),3,27],   149:[(mk4, mk3),4,28],   150:[(mk14, mk19),1,25], 151:[(mk15, mk0),2,26],  
        152:[(mk16, mk1),3,27],  153:[(mk9, mk4),1,25],   154:[(mk10, mk5),1,25],  155:[(mk17, mk3),2,26],  156:[(mk18, mk7),3,27],  157:[(mk19, mk3),4,28],  
        158:[(mk0, mk7),1,25],   159:[(mk1, mk8),2,26],   160:[(mk4, mk14),3,27],  161:[(mk19, mk15),4,28], 162:[(mk0, mk16),1,25],  163:[(mk1, mk9),2,26],   
        164:[(mk4, mk10),3,27],  165:[(mk5, mk17),4,28],  166:[(mk3, mk18),3,27],  167:[(mk7, mk19),4,28],  168:[(mk0, mk0),1,25],   169:[(mk1, mk1),2,26],   
        170:[(mk4, mk4),3,27],   171:[(mk17, mk5),1,25],  172:[(mk18, mk3),2,26],  173:[(mk19, mk7),3,27],  174:[(mk0, mk17),4,28],  175:[(mk1, mk18),1,25],  
        176:[(mk4, mk19),2,26],  177:[(mk9, mk0),3,27],   178:[(mk10, mk1),4,28],  179:[(mk17, mk4),1,25],  180:[(mk18, mk14),3,27], 181:[(mk19, mk15),1,25], 
        182:[(mk0, mk16),2,26],  183:[(mk1, mk9),3,27],   184:[(mk4, mk10),4,28],  185:[(mk14, mk17),3,27], 186:[(mk15, mk18),4,28], 187:[(mk16, mk19),4,28], 
        188:[(mk9, mk0),1,25],   189:[(mk10, mk1),2,26],  190:[(mk17, mk4),3,27],  191:[(mk18, mk19),4,28], 192:[(mk19, mk0),1,25],  193:[(mk0, mk1),2,26],   
        194:[(mk1, mk4),3,27],   195:[(mk4, mk14),4,28],  196:[(mk5, mk15),3,27],  197:[(mk3, mk16),4,28],  198:[(mk3, mk9),1,25],   199:[(mk7, mk1),2,26],   
        200:[(mk18, mk19),2,26], 201:[(mk19, mk0),3,27],  202:[(mk0, mk1),1,25],   203:[(mk1, mk4),2,26],   204:[(mk4, mk5),3,27],   205:[(mk14, mk3),4,28],  
        206:[(mk15, mk7),1,25],  207:[(mk16, mk17),2,26], 208:[(mk9, mk18),3,27],  209:[(mk10, mk19),4,28], 210:[(mk17, mk0),1,25],  211:[(mk18, mk1),3,27],  
        212:[(mk19, mk4),1,25],  213:[(mk0, mk14),2,26],  214:[(mk1, mk15),3,27],  215:[(mk4, mk16),4,28],  216:[(mk19, mk9),3,27],  217:[(mk0, mk10),4,28],  
        218:[(mk1, mk17),4,28],  219:[(mk4, mk18),1,25],  220:[(mk5, mk19),2,26],  221:[(mk3, mk0),3,27],   222:[(mk7, mk1),4,28],   223:[(mk0, mk4),1,25],   
        224:[(mk1, mk5),2,26],   225:[(mk4, mk3),3,27],   226:[(mk17, mk7),4,28],  227:[(mk18, mk17),2,26], 228:[(mk19, mk18),3,27], 229:[(mk0, mk19),1,25],  
        230:[(mk1, mk0),2,26],   231:[(mk4, mk1),3,27],   232:[(mk9, mk4),4,28],   233:[(mk10, mk14),1,25], 234:[(mk17, mk15),2,26], 235:[(mk18, mk16),3,27], 
        236:[(mk19, mk9),4,28],  237:[(mk0, mk10),1,25],  238:[(mk1, mk17),3,27],  239:[(mk4, mk19),1,25],  240:[(mk14, mk0),2,26],  241:[(mk15, mk1),3,27],  
        242:[(mk16, mk4),4,28],  243:[(mk9, mk5),3,27],   244:[(mk10, mk3),4,28],  245:[(mk17, mk7),4,28],  246:[(mk18, mk17),2,26], 247:[(mk19, mk18),3,27], 
        248:[(mk0, mk19),1,25],  249:[(mk1, mk0),2,26],   250:[(mk4, mk1),3,27],   251:[(mk19, mk4),4,28],  252:[(mk0, mk14),1,25],  253:[(mk1, mk15),2,26],  
        254:[(mk4, mk4),3,27],   255:[(mk5, mk14),4,28],  256:[(mk3, mk15),1,25],  257:[(mk7, mk16),3,27],  258:[(mk0, mk9),1,25],   259:[(mk1, mk10),2,26],  
        260:[(mk4, mk17),3,27],  261:[(mk17, mk18),4,28], 262:[(mk18, mk19),3,27], 263:[(mk19, mk0),4,28],  264:[(mk0, mk1),4,28],   265:[(mk1, mk4),1,25],   
        266:[(mk4, mk19),2,26],  267:[(mk9, mk0),3,27],   268:[(mk10, mk1),4,28],  269:[(mk17, mk4),1,25],  270:[(mk18, mk14),2,26], 271:[(mk19, mk15),3,27], 
        272:[(mk0, mk16),4,28],  273:[(mk1, mk9),3,27],   274:[(mk19, mk1),4,28],  275:[(mk0, mk19),1,25],  276:[(mk1, mk0),2,26],   277:[(mk4, mk1),2,26],   
        278:[(mk5, mk4),3,27],   279:[(mk3, mk5),1,25],   280:[(mk7, mk3),2,26],   281:[(mk17, mk7),3,27],  282:[(mk18, mk17),4,28], 283:[(mk19, mk18),1,25], 
        284:[(mk0, mk19),2,26],  285:[(mk1, mk0),3,27],   286:[(mk4, mk1),4,28],   287:[(mk14, mk4),1,25],  288:[(mk15, mk14),3,27], 289:[(mk16, mk15),1,25], 
        290:[(mk9, mk16),2,26],  291:[(mk10, mk9),3,27],  292:[(mk17, mk10),4,28], 293:[(mk18, mk17),3,27], 294:[(mk18, mk18),4,28], 295:[(mk19, mk19),4,28], 
        296:[(mk0, mk0),1,25],   297:[(mk1, mk1),2,26],   298:[(mk4, mk4),3,27],   299:[(mk5, mk5),4,28],   300:[(mk3, mk3),1,25],   301:[(mk7, mk7),2,26],   
        302:[(mk17, mk17),3,27], 303:[(mk18, mk18),4,28], 304:[(mk19, mk19),3,27], 305:[(mk0, mk0),4,28],   306:[(mk1, mk1),1,25],   307:[(mk4, mk4),2,26],   
        308:[(mk14, mk14),2,26], 309:[(mk15, mk15),3,27], 310:[(mk16, mk16),1,25], 311:[(mk9, mk9),2,26],   312:[(mk10, mk10),3,27], 313:[(mk17, mk17),4,28], 
        314:[(mk19, mk19),1,25], 315:[(mk0, mk0),2,26],   316:[(mk1, mk1),3,27],   317:[(mk4, mk4),4,28],   318:[(mk5, mk5),1,25],   319:[(mk3, mk3),3,27],   
        320:[(mk7, mk7),1,25],   321:[(mk17, mk17),2,26], 322:[(mk18, mk18),3,27], 323:[(mk19, mk19),4,28], 324:[(mk0, mk0),3,27],   325:[(mk1, mk1),4,28],   
        326:[(mk4, mk4),4,28],   327:[(mk19, mk14),1,25], 328:[(mk0, mk15),2,26],  329:[(mk1, mk16),3,27],  330:[(mk4, mk9),4,28],   331:[(mk19, mk10),1,25], 
        332:[(mk0, mk17),2,26],  333:[(mk1, mk18),3,27],  334:[(mk4, mk18),4,28],  335:[(mk5, mk19),3,27],  336:[(mk3, mk0),4,28],   337:[(mk7, mk1),2,26],   
        338:[(mk0, mk4),3,27],   339:[(mk1, mk5),1,25],   340:[(mk4, mk3),2,26],   341:[(mk17, mk7),3,27],  342:[(mk18, mk17),4,28], 343:[(mk19, mk18),1,25], 
        344:[(mk0, mk19),2,26],  345:[(mk1, mk0),3,27],   346:[(mk4, mk1),4,28],   347:[(mk9, mk4),1,25],   348:[(mk10, mk14),3,27], 349:[(mk17, mk15),1,25], 
        350:[(mk18, mk16),2,26], 351:[(mk19, mk9),3,27],  352:[(mk0, mk10),4,28],  353:[(mk1, mk17),3,27],  354:[(mk18, mk19),4,28], 355:[(mk19, mk0),4,28],  
        356:[(mk0, mk1),1,25],   357:[(mk1, mk4),2,26],   358:[(mk4, mk5),3,27],   359:[(mk5, mk3),4,28],   360:[(mk3, mk7),2,26],   361:[(mk7, mk17),3,27],  
        362:[(mk17, mk18),1,25], 363:[(mk18, mk19),2,26], 364:[(mk19, mk0),3,27],  365:[(mk0, mk1),4,28],   366:[(mk1, mk4),1,25],   367:[(mk4, mk7),2,26],   
        368:[(mk14, mk17),3,27], 369:[(mk15, mk18),4,28], 370:[(mk16, mk19),1,25], 371:[(mk9, mk0),3,27],   372:[(mk10, mk1),1,25],  373:[(mk17, mk4),2,26],  
        374:[(mk19, mk17),3,27], 375:[(mk0, mk18),4,28],  376:[(mk1, mk19),3,27],  377:[(mk4, mk0),4,28],   378:[(mk5, mk1),4,28],   379:[(mk3, mk4),1,25],   
        380:[(mk7, mk9),2,26],   381:[(mk17, mk10),3,27], 382:[(mk18, mk17),4,28], 383:[(mk19, mk18),1,25], 384:[(mk0, mk19),2,26],  385:[(mk1, mk0),3,27],   
        386:[(mk4, mk1),4,28],   387:[(mk17, mk1),2,26],  388:[(mk18, mk4),3,27],  389:[(mk19, mk7),1,25],  390:[(mk0, mk17),2,26],  391:[(mk1, mk18),3,27],  
        392:[(mk4, mk19),4,28],  393:[(mk9, mk0),1,25],   394:[(mk10, mk1),2,26],  395:[(mk17, mk4),3,27],  396:[(mk18, mk17),4,28], 397:[(mk19, mk18),1,25], 
        398:[(mk0, mk19),3,27],  399:[(mk1, mk0),1,25],
    }
    s = strToLong(cookie) % 400
    if s in e:
        return e[s](cookie)
    else:
        (f1,f2), l, r = d[s]
        return md5(f1(cookie) + f2(cookie))[l:r]

if __name__ == '__main__':
    print(getvl5x('3651a6394ff4969810151189b635aa414f945c77'))
