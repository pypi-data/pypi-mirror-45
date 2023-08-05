# THIS FILE IS GENERATED FROM PADDLEPADDLE SETUP.PY
#
full_version    = '1.4.0'
major           = '1'
minor           = '4'
patch           = '0'
rc              = '0'
istaged         = True
commit          = '2ff867f88628e9cb8b76eaf79045eca0f52e5b85'
with_mkl        = 'ON'

def show():
    if istaged:
        print('full_version:', full_version)
        print('major:', major)
        print('minor:', minor)
        print('patch:', patch)
        print('rc:', rc)
    else:
        print('commit:', commit)

def mkl():
    return with_mkl
