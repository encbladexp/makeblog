# Maintainer: Stefan J. Betz <info@stefan-betz.net>
pkgname=makeblog
pkgver=0.0.1
pkgrel=1
pkgdesc="A simple offline Blog."
arch=(any)
url="http://bitbucket.org/encbladexp/makeblog"
license=('GPL3')
options=(!emptydirs)
depends=('python-pytz' 'python-jinja' 'python-pygments')
source=($pkgname-$pkgver.tar.bz2)
md5sums=('966aae9f2902395237805a79e498e3a3')

package() {
	cd "$srcdir/$pkgname-$pkgver"
	python setup.py install --root="$pkgdir/" --optimize=1
}
