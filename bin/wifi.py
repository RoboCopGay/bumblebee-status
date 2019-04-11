from os import popen, system

def organize(cmd):
    cmd = '\\"'.join(cmd.split('<aspa>'))
    cmd = '\\|'.join(cmd.split('<pipe>'))
    return cmd

restart = True
while restart:
    restart = False
    try:
        redes = popen("nmcli device wifi list").read().split('\n')[1:]
        LINES = []
        for rede in redes:
            if rede.strip()!="":
                LINES.append(rede)
        LINES = ']!['.join(LINES)
    except:
        LINES = '' 
    LINES = '<aspa>'.join(LINES.split('"'))
    LINES = '<aspa>'.join(LINES.split("'"))
    LINES = '<pipe>'.join(LINES.split("|"))
    LINES = '|'.join(LINES.split("]!["))
        
    case = ''
    try:
        networks = open(popen("echo $HOME/.bin/network/connections").read().strip()).read().split(';')
    except:
        networks = []

    # mostrando as redes
    ssid = popen('echo \'echo "$(rofi -sep "|" -dmenu -i -p "Network" -hide-scrollbar -line-padding 4 -padding 20 -lines {} <<< "{}")"\'> $HOME/.bin/network/script;bash $HOME/.bin/network/script'.format( len(LINES.split("|")), organize(LINES))).read().strip()

    if ssid.strip()=="":
        exit(1)

    # senhas salvas
    con = {}
    for net in open(popen("echo $HOME/.bin/network/connections").read().strip()).read().strip().split(';'):
        try:
            con[net.split(":")[0].strip()] = net.split(":")[1].strip()
        except:
            pass

    if "*" in ssid:
        ssid = ssid.strip().split()[1:]
        for char in ssid:
            if char.strip()!="":
                ssid = char
                break
    else:
        ssid = ssid.strip().split()[0]

    # caso a senha não esteja salva
    if ssid not in con:
        password = popen('echo \'echo "$(rofi -sep "|" -dmenu -i -p "Password" -width 40 -hide-scrollbar -line-padding 4 -padding 20 -lines 1 <<< "Cancel" )"\' > $HOME/.bin/network/passquestion;bash $HOME/.bin/network/passquestion').read().strip()
        if password=="Cancel":
            exit(0)
    else:
        # caso a senha esteja no banco de dados
        password = con[ssid].strip()

    script = r"nmcli device wifi connect '{}' password '{}'".format(ssid.strip(), password.strip())

    # caso a senha esteja errada
    sair = False
    try:
        if not "erro" in popen(script).read().lower():
            sair = True
        else:
            sair = False
    except:
        sair = False

    if sair:
        print("connected with ssid:",ssid, "password:",password)
        system( "notify-send -u normal Wifi 'connected in \"{}\"'".format(ssid) )

        # a senha soh serah registrada se a coneccao for bem sucedida
        con[ssid.strip()] = password.strip()

        conhistory = ''
        for connection in con:
            if con[connection].strip() != '':
                conhistory += "{}:{};".format(connection,con[connection])
        open(popen("echo $HOME/.bin/network/connections").read().strip(), 'w').write(conhistory)
        exit(0)


    count = 0
    while not sair or count<5:
        system("notify-send -u normal Wifi 'a senha esta errada ou voce esta muito longe do roteador!'")
        password = popen('echo \'echo "$(rofi -sep "|" -dmenu -i -p "Password" -width 40 -hide-scrollbar -line-padding 4 -padding 20 -lines 3 <<< "last tryed: \\"{}\\"|Select other network|Cancel" )"\' > $HOME/.bin/network/passquestion;bash $HOME/.bin/network/passquestion'.format(password)).read().strip()

        # caso a pessoa queira cancelar
        if password.strip()=="Cancel":
            exit(1)
        if password.strip()=='Select other network':
            restart = True
            break
        
        if ":" in password:
            password = ''.join(password[password.index(":")+1:]).strip()

        script = r"nmcli device wifi connect '{}' password '{}'".format(ssid.strip(), password.strip())
        
        try:
            if not "erro" in popen(script).read().lower():
                sair = True
            else:
                sair = False
        except:
            sair = False
        
        if sair:
            print("connected with ssid:",ssid, "password:",password)
            system( "notify-send -u normal Wifi 'connected in \"{}\"'".format(ssid) )

            # a senha soh serah registrada se a coneccao for bem sucedida
            con[ssid.strip()] = password.strip()

            conhistory = ""
            for connection in con:
                if con[connection].strip() != '':
                    conhistory += "{}:{};".format(connection,con[connection])
            open(popen("echo $HOME/.bin/network/connections").read().strip(), 'w').write(conhistory)
            exit(0)
        count += 1


