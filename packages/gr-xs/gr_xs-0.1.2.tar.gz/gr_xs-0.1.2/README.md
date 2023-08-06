# gr_xs
Implementation of arxiv:1407.4415 for nu-e W-Boson resonance with Doppler broadening.

Install via `pip install gr-xs`.

```Python
import gr_xs
gr_xs.sigma_erest(6.3e6) # Eq. (3), cross-section ratio of electron at rest
gr_xs.sigma_edopp(6.3e6, 'O') # Eq. (6), cross-section ratio of bound electron in O
```
