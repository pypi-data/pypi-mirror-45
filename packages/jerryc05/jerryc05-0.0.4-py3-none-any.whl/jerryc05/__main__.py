def main():
    from sys import argv
    argv: list
    if len(argv) == 1:
        argv.append(None)
    from jerryc05.my_12306.__main__ import main as main_12306
    # todo

    {
        '12306': lambda: main_12306(argv[1:]),
        None: lambda: print('''
                                  .. .vr 
                                qBMBBBMBMY 
                               8BBBBBOBMBMv 
                             iMBMM5vOY:BMBBv 
             .r,             OBM;   .: rBBBBBY 
             vUL             7BB   .;7. LBMMBBM. 
            .@Wwz.           :uvir .i:.iLMOMOBM.. 
             vv::r;             iY. ...rv,@arqiao. 
              Li. i:             v:.::::7vOBBMBL.. 
              ,i7: vSUi,         :M7.:.,:u08OP. . 
                .N2k5u1ju7,..     BMGiiL7   ,i,i. 
                 :rLjFYjvjLY7r::.  ;v  vr... rE8q;.:,, 
                751jSLXPFu5uU@guohezou.,1vjY2E8@Yizero. 
                BB:FMu rkM8Eq0PFjF15FZ0Xu15F25uuLuu25Gi. 
              ivSvvXL    :v58ZOGZXF2UUkFSFkU1u125uUJUUZ, 
            :@kevensun.      ,iY20GOXSUXkSuS2F5XXkUX5SEv. 
        .:i0BMBMBBOOBMUi;,        ,;8PkFP5NkPXkFqPEqqkZu. 
      .rqMqBBMOMMBMBBBM .           @kexianli.S11kFSU5q5 
    .7BBOi1L1MM8BBBOMBB..,          8kqS52XkkU1Uqkk1kUEJ 
    .;MBZ;iiMBMBMMOBBBu ,           1OkS1F1X5kPP112F51kU 
      .rPY  OMBMBBBMBB2 ,.          rME5SSSFk1XPqFNkSUPZ,. 
             ;;JuBML::r:.:.,,        SZPX0SXSP5kXGNP15UBr. 
                 L,    :@huhao.      :MNZqNXqSqXk2E0PSXPE . 
             viLBX.,,v8Bj. i:r7:,     2Zkqq0XXSNN0NOXXSXOU 
           :r2. rMBGBMGi .7Y, 1i::i   vO0PMNNSXXEqP@Secbone. 
           .i1r. .jkY,    vE. iY....  20Fq0q5X5F1S2F22uuv1M;
''')
    }.get(argv[1] if argv[1] == None or type(argv[1]) == str else f'{argv[1]}',
          lambda: print(f'Argument {argv[1]} invalid'))()


if __name__ == "__main__":
    main()
