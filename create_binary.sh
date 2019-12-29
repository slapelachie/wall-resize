cd ./src/
zip -r ../wall-resize.zip *
cd ..
echo '#!/usr/bin/env python' | cat - wall-resize.zip > wall-resize
chmod +x wall-resize
rm wall-resize.zip