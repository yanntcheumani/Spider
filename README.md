# Spiders
   <blockquote>
        <p>
            Find usernames across social networks
            <a href="">social network</a>
            </p>
   </blockquote>
   <h2>Installation</h2>
   <strong>Notes</strong>: Python 3.6 or higher is required.
   <div class="highlight highlight-source-shell"><pre><span class="pl-c"><span class="pl-c">#</span> clone the repository</span>
$ git clone https://github.com/yanntcheumani/spiders.git

<span class="pl-c"><span class="pl-c">#</span> change the working directory to spiders</span>
$ <span class="pl-c1">cd</span> spiders

<span class="pl-c"><span class="pl-c">#</span> install the requirements</span>
$ pip3 install -r requirements.txt</pre></div>
------------
<h2>Utilisations</h2>
<div class="highlight highlight-source-shell"><pre>
(venv) C:\Users\Anonyme\PycharmProjects\Spiders>py spider.py --help
usage: spider.py [-h] [--version] [--verbose] [--site SITE_NAME]
                 Pseudo [Pseudo ...]

Spider: Find Usernames Across Social Networks (Version 1.0)

positional arguments:
  Pseudo                One or more usernames to check with social networks.

optional arguments:
  -h, --help            show this help message and exit
  --version             Display version information and dependencies.
  --verbose, -v, -d, --debug
                        Display extra debugging information and metrics.
  --site SITE_NAME      Limit analysis to just the listed sites. Add multiple
                        options to specify more than one site.
</pre>

---------------
<p>For example, run <code>python3 spider.py yann_tcheumani</code></p>
<h2>Views</h2>
<a target="_blank" rel="noopener noreferrer" href="/yanntcheumani/Hack/blob/master/screenshot/preview.png">
<img src="/yanntcheumani/Spider/raw/master/screenshot/preview.png" style="max-width:100%;"></a>
