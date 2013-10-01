# Maintainer: Stefan J. Betz <info@stefan-betz.net>
pkgname=makeblog
pkgver=0.0.2
pkgrel=1
pkgdesc="A simple offline Blog."
arch=(any)
url="http://bitbucket.org/encbladexp/makeblog"
license=('GPL3')
options=(!emptydirs)
depends=('python-pytz' 'python-jinja' 'python-pygments')
source=(https://bitbucket.org/encbladexp/$pkgname/get/$pkgver.tar.bz2)
md5sums=('d0c3dba64d9e448c8a47f3c194d28257')

package() {
	cd "$srcdir/encbladexp-$pkgname-98d250941c28"
	python setup.py install --root="$pkgdir/" --optimize=1
}
