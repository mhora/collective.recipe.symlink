import logging
logger = logging.getLogger('symlinks')

import os

import zc.buildout
import zc.recipe.egg

class Recipe(object):

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        
        self.options['eggs-directory'] = buildout['buildout']['eggs-directory']
        self.options['python'] = self.buildout['buildout']['python']
        self.options['executable'] = self.buildout[self.options['python']]['executable']
        self.options['eggs-directory'] = buildout['buildout']['eggs-directory']

    def install(self):
        return self.create_symlinks()

    def update(self):
        return self.install()

    def install_egg(self, egg):
        """Installs the specified `egg`."""
        links = self.buildout['buildout'].get('find-links', [])
        if links:
            links = tuple(links.split('\n'))
        ws = zc.buildout.easy_install.install(
            [egg], self.options['eggs-directory'],
            links           = links,
            index           = self.buildout['buildout'].get('index'),
            executable      = self.options['executable'],
            path            = [self.options['eggs-directory']],
            newest          = self.buildout['buildout'].get('newest') == 'true',
            allow_hosts     = self.buildout['buildout'].get('allow-hosts', '*'),
            always_unzip    = 'true', )
        return ws.require(egg)[0].location
    

    def create_symlinks(self):

        egg = self.options['egg']
        destination = self.options['destination']
         
        if os.path.exists(destination):
            if not os.path.isdir(destination):
                logger.error("ERROR: The destination %s already exists and is not a directory" % destination)
                logger.info("Creating symbolic links failed")
                return ()
        else:
            os.makedirs(destination)
            logger.info("Created %s directory" % destination)

        raw_symlinks = self.options['links']
        ws = zc.recipe.egg.Egg(self.buildout, egg, self.options).working_set()
        location = ws[1].by_key[egg.lower()].location 

        files = []
        symlinks = raw_symlinks.split('\n')
        for symlink in symlinks:
            if not symlink:
                # Empty lines
                continue
            
            raw_dest, raw_src  = symlink.split('=')
            src = os.path.join(location, raw_src.strip())
            dest = os.path.join(destination, raw_dest.strip())

            # This is save as it will raise an error if it is not a link
            try:
                os.unlink(dest)
            except OSError:
                pass

            os.symlink(src, dest)
            logger.info("Linked %s to %s" % (src, dest))
            files.append(dest)

        return files
