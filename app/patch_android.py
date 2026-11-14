"""Customise the generated Capacitor Android project:
- block screenshots / screen recording (FLAG_SECURE)
- install launcher icons
- set version from env (VERSION_CODE / VERSION_NAME)
"""
import os, re, shutil, glob

root = 'android/app/src/main'
java = glob.glob(f'{root}/java/**/MainActivity.java', recursive=True)[0]
src = open(java, encoding='utf-8').read()
if 'FLAG_SECURE' not in src:
    src = src.replace('import com.getcapacitor.BridgeActivity;',
        'import android.os.Bundle;\nimport android.view.WindowManager;\nimport com.getcapacitor.BridgeActivity;')
    src = re.sub(r'public class MainActivity extends BridgeActivity \{\s*\}',
        'public class MainActivity extends BridgeActivity {\n'
        '    @Override\n'
        '    public void onCreate(Bundle savedInstanceState) {\n'
        '        super.onCreate(savedInstanceState);\n'
        '        getWindow().setFlags(WindowManager.LayoutParams.FLAG_SECURE, WindowManager.LayoutParams.FLAG_SECURE);\n'
        '    }\n'
        '}', src)
    assert 'FLAG_SECURE' in src, 'MainActivity patch failed'
    open(java, 'w', encoding='utf-8').write(src)

# icons: use plain PNG launcher icons (drop adaptive xml)
shutil.rmtree(f'{root}/res/mipmap-anydpi-v26', ignore_errors=True)
for d in glob.glob('res/mipmap-*'):
    dst = f'{root}/res/{os.path.basename(d)}'
    os.makedirs(dst, exist_ok=True)
    for f in glob.glob(f'{d}/*.png'):
        shutil.copy(f, dst)
for f in glob.glob(f'{root}/res/mipmap-*/ic_launcher_foreground.png'):
    os.remove(f)

g = 'android/app/build.gradle'
s = open(g, encoding='utf-8').read()
s = re.sub(r'versionCode \d+', 'versionCode ' + os.environ.get('VERSION_CODE', '1'), s)
s = re.sub(r'versionName "[^"]*"', 'versionName "' + os.environ.get('VERSION_NAME', '1.0') + '"', s)
open(g, 'w', encoding='utf-8').write(s)
print('patched', java)
