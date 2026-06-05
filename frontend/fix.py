import os
import glob

files = glob.glob('src/**/*.ts*', recursive=True)
for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    if 'import { Matter' in content or 'import { Document' in content:
        content = content.replace('import { Matter', 'import type { Matter')
        content = content.replace('import { Document', 'import type { Document')
        
    with open(file, 'w') as f:
        f.write(content)
