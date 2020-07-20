from pysmi.reader import HttpReader
from pysmi.reader import FtpReader
from pysmi.reader import FileReader
from pysmi.searcher import StubSearcher
from pysmi.writer import PyFileWriter
from pysmi.parser import SmiStarParser
from pysmi.codegen import PySnmpCodeGen
from pysmi.compiler import MibCompiler

inputMibs = ['IF-MIB', 'BRIDGE-MIB','LUXL-POE-MIB','LUXL-SMI','LUXL-TC']
httpSources = [
    ('mibs.snmplabs.com', 80, '/asn1/@mib@')
]
ftpSources = [
    ('ftp.cisco.com', '/pub/mibs/v2/@mib@')
]
srcDirectories = [
    ('./LUXL_MIBs_ALL')
]
dstDirectory = './lib/python3.7/site-packages/pysnmp/smi/mibs/'

# Initialize compiler infrastructure

mibCompiler = MibCompiler(
    SmiStarParser(), PySnmpCodeGen(), PyFileWriter(dstDirectory)
)

# search for source MIBs at Web and FTP sites
mibCompiler.addSources(*[HttpReader(*x) for x in httpSources])
mibCompiler.addSources(*[FtpReader(*x) for x in ftpSources])
mibCompiler.addSources(*[FileReader(x) for x in srcDirectories])

# never recompile MIBs with MACROs
mibCompiler.addSearchers(StubSearcher(*PySnmpCodeGen.baseMibs))

# run non-recursive MIB compilation
results = mibCompiler.compile(*inputMibs, **dict(noDeps=True))

print('Results: %s' % ', '.join(['%s:%s' % (x, results[x]) for x in results]))