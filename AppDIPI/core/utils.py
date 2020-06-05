# fonte:  https://wiki.python.org.br/VerificadorDeCPF

import re

# traduz 123.456.789-10 para 12345678910
_translate = lambda cpf: ''.join(re.findall("\d", cpf))

invalidos = ('00000000000', '11111111111', '22222222222', '33333333333',
    '44444444444', '55555555555', '66666666666', '77777777777', '88888888888', '99999999999')

def _exceptions(cpf):
    """
    Se o número de CPF estiver dentro das exceções é inválido

    """
    if len(cpf)!=11:
        return True
    else:
        s=''.join(str(x) for x in cpf)
        if s in invalidos:
            return True
    return False

def _gen(cpf):
    """
    Gera o próximo dígito do número de CPF

    """
    res = []
    for i, a in enumerate(cpf):
        b = len(cpf) + 1 - i
        res.append(b * a)

    res = sum(res) % 11

    if res > 1:
        return 11 - res
    else:
        return 0


class CPF(object):

    _gen = staticmethod(_gen)
    _translate = staticmethod(_translate)
    
    def __init__(self, cpf):
        """O argumento cpf pode ser uma string nas formas:

        12345678910
        123.456.789-10

        ou uma lista ou tuple
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 0]
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 0)

        """
        
        if isinstance(cpf, str):
            if not cpf.isdigit():
               cpf = self._translate(cpf)
            
        self.cpf = [int(x) for x in cpf]

    def __getitem__(self, index):
        """Retorna o dígito em index como string

        """
        
        return self.cpf[index]

    def __repr__(self):
        """Retorna uma representação 'real', ou seja:

        eval(repr(cpf)) == cpf
        
        """
        
        return "CPF('%s')" % ''.join(str(x) for x in self.cpf)

    def __eq__(self, other):
        """Provê teste de igualdade para números de CPF

        """

        return isinstance(other, CPF) and self.cpf == other.cpf
    
    def __str__(self):
        """Retorna uma representação do CPF na forma:

        123.456.789-10

        """

        d = iter("..-")
        s = map(str, self.cpf)
        for i in xrange(3, 12, 4):
            s.insert(i, d.next())
        r = ''.join(s)
        return r

    def isValid(self):
        """Valida o número de cpf

        """
        
        if _exceptions(self.cpf):
            return False

        s = self.cpf[:9]
        s.append(self._gen(s))
        s.append(self._gen(s))
        return s == self.cpf[:]



class Cnpj:
    def __init__( self ):
        """
        Class to interact with Cnpj brazilian numbers
        """
        pass
        
    def validate( self, cnpj ):
        """ 
        Method to validate brazilian cnpjs
        Tests:
        
        >>> print Cnpj().validate('61882613000194')
        True
        >>> print Cnpj().validate('61882613000195')
        False
        >>> print Cnpj().validate('53.612.734/0001-98')
        True
        >>> print Cnpj().validate('69.435.154/0001-02')
        True
        >>> print Cnpj().validate('69.435.154/0001-01')
        False
        """
        # defining some variables
        lista_validacao_um = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4 , 3, 2]
        lista_validacao_dois = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        
        # cleaning the cnpj
        cnpj = cnpj.replace( "-", "" )
        cnpj = cnpj.replace( ".", "" )
        cnpj = cnpj.replace( "/", "" )
    
        # finding out the digits
        verificadores = cnpj[-2:]
        
        # verifying the lenght of the cnpj
        if len( cnpj ) != 14:
            return False
        
        # calculating the first digit
        soma = 0
        id = 0
        for numero in cnpj:
            
            # to do not raise indexerrors
            try:
                lista_validacao_um[id]
            except:
                break
                
            soma += int( numero ) * int( lista_validacao_um[id] )
            id += 1
        
        soma = soma % 11
        if soma < 2:
            digito_um = 0
        else:
            digito_um = 11 - soma
        
        digito_um = str( digito_um ) # converting to string, for later comparison
        
        # calculating the second digit
        # suming the two lists
        soma = 0
        id = 0
        
        # suming the two lists
        for numero in cnpj:
            
            # to do not raise indexerrors
            try:
                lista_validacao_dois[id]
            except:
                break
            
            soma += int( numero ) * int( lista_validacao_dois[id] )
            id += 1
        
        # defining the digit
        soma = soma % 11
        if soma < 2:
            digito_dois = 0
        else:
            digito_dois = 11 - soma
        
        digito_dois = str( digito_dois )
    
        # returnig
        return bool( verificadores == digito_um + digito_dois )

    def format( self, cnpj ):
        """
        Method to format cnpj numbers.
        Tests:
        
        >>> print Cnpj().format('53612734000198')
        53.612.734/0001-98
        """
        return "%s.%s.%s/%s-%s" % ( cnpj[0:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:14] )

