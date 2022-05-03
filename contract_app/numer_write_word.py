
def sonn(numer):
    if numer<1000 and numer>0:
        result=''
        son=numer//100
        if son==1:
            result='bir yuz'
        elif son==2:
            result='ikki yuz'
        elif son==3:
            result='uch yuz'
        elif son==4:
            result='to\'rt yuz'
        elif son==5:
            result='bech yuz'
        elif son==6:
            result='olti yuz'
        elif son==7:
            result='yetti yuz'
        elif son==8:
            result='sakiz yuz'
        elif son==9:
            result='to\'qiz yuz'
        num=numer%100
        qoliq=num%10
        if num>9 and num<=19:
            result+=' o\'n'
        elif num>19 and num <=29:
            result+=' yigirma'
        elif num>29 and num <=39:
            result+=' o\'tiz'
        elif num>39 and num <=49:
            result+=' qirq'
        elif num>49 and num <=59:
            result+=' elik'
        elif num>59 and num <=69:
            result+=' oltmish'
        elif num>69 and num <=79:
            result+=' yetmish'
        elif num>79 and num <=89:
            result+=' sakson'
        elif num>89 and num <=99:
            result+=' to\'qson'
        if qoliq==1:
            result+=' bir'
        elif qoliq==2:
            result+=' ikki'
        elif qoliq==3:
            result+=' uch'
        elif qoliq==4:
            result+=' to\'rt'
        elif qoliq==5:
            result+=' besh'
        elif qoliq==6:
            result+=' olti'
        elif qoliq==7:
            result+=' yetti'
        elif qoliq==8:
            result+=' sakkiz'
        elif qoliq==9:
            result+=' to\'qiz'
        return result
    else:
        return False

        
def son(number):
    tyin=str(number).split('.')

    if len(tyin)>1:
        tyin=int(tyin[1])
        length=tyin
    else:
        tyin=0
        length=0
    number=int(number)
    numberic=['  ',' yuz ',' ming ',' million ', ' milliard ',' trillon ']
    numberic2=[1,100,1000,1000000,1000000000,1000000000000,1000000000000000]
    s=''
    i=1
    while number!=0:
        n=number%numberic2[i]
        if n//numberic2[i-1]!=0:
            j=sonn(n//numberic2[i-1])+numberic[i-1]
            j+=s
            s=j
                
        number=number-n
        i+=1
    s+='so\'m,'
    u=''
 
    i=0
    print(tyin)
    while tyin!=0:
        n=tyin%numberic2[i]
        if n//numberic2[i-1]!=0:
            j=sonn(n//numberic2[i-1])+numberic[i-1]
            j+=u
            u=j 
        tyin=tyin-n
        i+=1
    if length>0:
        u+='tiyin'
    s+=u
    return s
def float2comma(f):
    s = str(abs(f)) # Convert to a string
    decimalposition = s.find(".") # Look for decimal point
    if decimalposition == -1:
        decimalposition = len(s) # If no decimal, then just work from the end
    out = "" 
    for i in range(decimalposition+1, len(s)): # do the decimal
        if not (i-decimalposition-1) % 3 and i-decimalposition-1: out = out+","
        out = out+s[i]      
    if len(out):
        out = "."+out # add the decimal point if necessary
    for i in range(decimalposition-1,-1,-1): # working backwards from decimal point
        if not (decimalposition-i-1) % 3 and decimalposition-i-1: out = ","+out
        out = s[i]+out      
    if f < 0:
        out = "-"+out
    return out