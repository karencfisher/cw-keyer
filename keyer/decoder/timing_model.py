class TimingModel:
    def __init__(self):
        self.dit_ms = None
        self.dah_ms = None
        self.ready = False

    def try_bootstrap(self, down_durations: list[int]) -> bool:
        for i, d1 in enumerate(down_durations):
            for d2 in down_durations[i + 1:]:
                short = min(d1, d2)
                long = max(d1, d2)

                if short == 0:
                    continue

                ratio = long / short

                if 2.5 <= ratio <= 3.5:
                    self.dit_ms = short
                    self.dah_ms = long
                    self.ready = True
                    self.refine_centers(down_durations)
                    return True
        return False

    def refine_centers(self, down_times):
        dits = []
        dahs = []

        # classify this batch using current centers
        for d in down_times:
            dit_err = abs(d - self.dit_ms) / self.dit_ms
            dah_err = abs(d - self.dah_ms) / self.dah_ms

            if dit_err < dah_err:
                dits.append(d)
            else:
                dahs.append(d)

        # don't update from a useless batch
        if not dits or not dahs:
            return False

        # proposed new centers
        new_dit = sum(dits) / len(dits)
        new_dah = sum(dahs) / len(dahs)

        # sanity check the proposed update
        ratio = new_dah / new_dit
        if not (2.2 <= ratio <= 4.2):
            return False

        # accept update
        self.dit_ms = new_dit
        self.dah_ms = new_dah
        return True
        