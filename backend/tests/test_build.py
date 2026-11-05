import subprocess
from pathlib import Path

def test_package_build():
    # Run your build command, e.g., standard Python build
    result = subprocess.run(
        ["python", "-m", "build"],
        capture_output=True,
        text=True,
    )
    
    # Assert the process exited with a zero (success) code
    assert result.returncode == 0, f"Build failed with stderr:\n{result.stderr}"
    
    # Optionally verify that the output artifact (wheel/tarball) was created
    dist_dir = Path("dist")
    wheels = list(dist_dir.glob("*.whl"))
    assert len(wheels) > 0, "No wheel file was generated in dist/"
