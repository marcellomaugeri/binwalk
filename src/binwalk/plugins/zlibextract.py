import os
import zlib
import binwalk.core.common
import binwalk.core.plugin

class ZLIBExtractPlugin(binwalk.core.plugin.Plugin):
    '''
    Zlib extractor plugin.
    '''
    MODULES = ['Signature']

    def init(self):
        # If the extractor is enabled for the module we're currently loaded
        # into, then register self.extractor as a zlib extraction rule.
        if self.module.extractor.enabled:
            self.module.extractor.add_rule(txtrule=None,
                                           regex="^zlib compressed data",
                                           extension="zlib",
                                           cmd=self.extractor)

    def extractor(self, fname):
        outfile = os.path.splitext(fname)[0]
        #print ("Extracting from '%s' to '%s'" % (fname, outfile))

        try:
            fpin = binwalk.core.common.BlockFile(fname)
            fpout = binwalk.core.common.BlockFile(outfile, 'w')

            plaintext = zlib.decompress(fpin.read())
            fpout.write(plaintext)

            fpin.close()
            fpout.close()
        except Exception, e:
            pass
            #print ("Failed to decompress data:", str(e))

