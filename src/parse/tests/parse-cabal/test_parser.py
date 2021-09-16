import os
import subprocess


def build_metadata(data):
    return {
        'name': data[0],
        'version': data[1],
        'stability': list(map(lambda x: x.strip().lower(), data[2].replace('"', "").split(','))),
        'category': list(map(lambda x: x.strip().lower(), data[3].replace('"', "").split(','))),
        'cabal_file_path': data[4],
        'dependencies': data[5].split(','),
        'provided_modules': data[6],
        'src-dirs': data[7],
        'main-modules': data[8]
    }


def run_parser(case_path):
    complated_process = subprocess.run(
        os.path.join(os.path.dirname(__file__), "../../ParseCabal"),
        stdout=subprocess.PIPE,
        input=case_path,
        text=True,
    )

    return complated_process.stdout


def test_bytestring():
    cabal_file = os.path.join(os.path.dirname(
        __file__), "inputs/bytestring.cabal")
    result = run_parser(cabal_file).split(";")
    metadata = build_metadata(result)
    dependencies_version = list(
        map(lambda x: tuple(x.split(' ', 1)), metadata['dependencies']))

    assert dependencies_version == [('base', '>=4.9 && <5'), (
        'deepseq', '-any'), ('ghc-prim', '-any'), ('template-haskell', '-any')]


def test_aws():
    cabal_file = os.path.join(os.path.dirname(__file__), "inputs/aws.cabal")
    result = run_parser(cabal_file).split(";")
    metadata = build_metadata(result)
    dependencies_version = list(
        map(lambda x: tuple(x.split(' ', 1)), metadata['dependencies']))

    assert dependencies_version == [('aeson', '>=0.6'),
                                    ('attoparsec', '>=0.11 && <0.14'),
                                    ('base', '>=4.6 && <5'),
                                    ('base16-bytestring', '==0.1.*'),
                                    ('base64-bytestring', '==1.0.*'),
                                    ('blaze-builder', '>=0.2.1.4 && <0.5'),
                                    ('byteable', '==0.1.*'),
                                    ('bytestring', '>=0.9 && <0.11'),
                                    ('case-insensitive', '>=0.2 && <1.3'),
                                    ('cereal', '>=0.3 && <0.6'),
                                    ('conduit', '==1.3.*'),
                                    ('conduit-extra', '==1.3.*'),
                                    ('containers', '>=0.4'),
                                    ('cryptonite', '>=0.11'),
                                    ('data-default', '>=0.5.3 && <0.8'),
                                    ('directory', '>=1.0 && <2.0'),
                                    ('exceptions', '>=0.8 && <0.11'),
                                    ('filepath',  '>=1.1 && <1.5'),
                                    ('http-client-tls', '==0.3.*'),
                                    ('http-conduit', '==2.3.*'),
                                    ('http-types', '>=0.7 && <1.0'),
                                    ('lifted-base', '>=0.1 && <0.3'),
                                    ('memory', '-any'),
                                    ('monad-control', '>=0.3'),
                                    ('mtl', '==2.*'),
                                    ('old-locale', '==1.*'),
                                    ('resourcet', '==1.2.*'),
                                    ('safe', '==0.3.*'),
                                    ('scientific', '>=0.3'),
                                    ('tagged', '>=0.7 && <0.9'),
                                    ('text', '>=0.11'),
                                    ('time', '>=1.4.0 && <2.0'),
                                    ('transformers', '>=0.2.2 && <0.6'),
                                    ('unordered-containers', '>=0.2'),
                                    ('utf8-string', '>=0.3 && <1.1'),
                                    ('vector', '>=0.10'),
                                    ('xml-conduit', '>=1.8 && <2.0')]
