"use client";

/**
 * The periodic table, as the real exam provides it in Chemical and Physical
 * Foundations: atomic number, symbol and atomic weight, in the standard
 * layout, opened and closed over the question.
 *
 * Atomic weights are IUPAC's 2021 standard values, rounded the way the AAMC's
 * on-screen table rounds them.
 */
const ELEMENTS: [number, string, string, number, number][] = [
  [1, "H", "1.0", 1, 1], [2, "He", "4.0", 1, 18],
  [3, "Li", "6.9", 2, 1], [4, "Be", "9.0", 2, 2], [5, "B", "10.8", 2, 13], [6, "C", "12.0", 2, 14], [7, "N", "14.0", 2, 15], [8, "O", "16.0", 2, 16], [9, "F", "19.0", 2, 17], [10, "Ne", "20.2", 2, 18],
  [11, "Na", "23.0", 3, 1], [12, "Mg", "24.3", 3, 2], [13, "Al", "27.0", 3, 13], [14, "Si", "28.1", 3, 14], [15, "P", "31.0", 3, 15], [16, "S", "32.1", 3, 16], [17, "Cl", "35.5", 3, 17], [18, "Ar", "39.9", 3, 18],
  [19, "K", "39.1", 4, 1], [20, "Ca", "40.1", 4, 2], [21, "Sc", "45.0", 4, 3], [22, "Ti", "47.9", 4, 4], [23, "V", "50.9", 4, 5], [24, "Cr", "52.0", 4, 6], [25, "Mn", "54.9", 4, 7], [26, "Fe", "55.8", 4, 8], [27, "Co", "58.9", 4, 9], [28, "Ni", "58.7", 4, 10], [29, "Cu", "63.5", 4, 11], [30, "Zn", "65.4", 4, 12], [31, "Ga", "69.7", 4, 13], [32, "Ge", "72.6", 4, 14], [33, "As", "74.9", 4, 15], [34, "Se", "79.0", 4, 16], [35, "Br", "79.9", 4, 17], [36, "Kr", "83.8", 4, 18],
  [37, "Rb", "85.5", 5, 1], [38, "Sr", "87.6", 5, 2], [39, "Y", "88.9", 5, 3], [40, "Zr", "91.2", 5, 4], [41, "Nb", "92.9", 5, 5], [42, "Mo", "96.0", 5, 6], [43, "Tc", "(98)", 5, 7], [44, "Ru", "101.1", 5, 8], [45, "Rh", "102.9", 5, 9], [46, "Pd", "106.4", 5, 10], [47, "Ag", "107.9", 5, 11], [48, "Cd", "112.4", 5, 12], [49, "In", "114.8", 5, 13], [50, "Sn", "118.7", 5, 14], [51, "Sb", "121.8", 5, 15], [52, "Te", "127.6", 5, 16], [53, "I", "126.9", 5, 17], [54, "Xe", "131.3", 5, 18],
  [55, "Cs", "132.9", 6, 1], [56, "Ba", "137.3", 6, 2], [57, "La", "138.9", 6, 3], [72, "Hf", "178.5", 6, 4], [73, "Ta", "180.9", 6, 5], [74, "W", "183.8", 6, 6], [75, "Re", "186.2", 6, 7], [76, "Os", "190.2", 6, 8], [77, "Ir", "192.2", 6, 9], [78, "Pt", "195.1", 6, 10], [79, "Au", "197.0", 6, 11], [80, "Hg", "200.6", 6, 12], [81, "Tl", "204.4", 6, 13], [82, "Pb", "207.2", 6, 14], [83, "Bi", "209.0", 6, 15], [84, "Po", "(209)", 6, 16], [85, "At", "(210)", 6, 17], [86, "Rn", "(222)", 6, 18],
  [87, "Fr", "(223)", 7, 1], [88, "Ra", "(226)", 7, 2], [89, "Ac", "(227)", 7, 3], [104, "Rf", "(265)", 7, 4], [105, "Db", "(268)", 7, 5], [106, "Sg", "(271)", 7, 6], [107, "Bh", "(272)", 7, 7], [108, "Hs", "(277)", 7, 8], [109, "Mt", "(276)", 7, 9], [110, "Ds", "(281)", 7, 10], [111, "Rg", "(280)", 7, 11], [112, "Cn", "(285)", 7, 12], [113, "Nh", "(286)", 7, 13], [114, "Fl", "(289)", 7, 14], [115, "Mc", "(289)", 7, 15], [116, "Lv", "(293)", 7, 16], [117, "Ts", "(294)", 7, 17], [118, "Og", "(294)", 7, 18],
];

const LANTHANIDES: [number, string, string][] = [
  [58, "Ce", "140.1"], [59, "Pr", "140.9"], [60, "Nd", "144.2"], [61, "Pm", "(145)"], [62, "Sm", "150.4"], [63, "Eu", "152.0"], [64, "Gd", "157.3"],
  [65, "Tb", "158.9"], [66, "Dy", "162.5"], [67, "Ho", "164.9"], [68, "Er", "167.3"], [69, "Tm", "168.9"], [70, "Yb", "173.0"], [71, "Lu", "175.0"],
];

const ACTINIDES: [number, string, string][] = [
  [90, "Th", "232.0"], [91, "Pa", "231.0"], [92, "U", "238.0"], [93, "Np", "(237)"], [94, "Pu", "(244)"], [95, "Am", "(243)"], [96, "Cm", "(247)"],
  [97, "Bk", "(247)"], [98, "Cf", "(251)"], [99, "Es", "(252)"], [100, "Fm", "(257)"], [101, "Md", "(258)"], [102, "No", "(259)"], [103, "Lr", "(262)"],
];

function Cell({ number, symbol, weight }: { number: number; symbol: string; weight: string }) {
  return (
    <div className="pt-cell">
      <span className="pt-number">{number}</span>
      <strong className="pt-symbol">{symbol}</strong>
      <span className="pt-weight">{weight}</span>
    </div>
  );
}

export default function PeriodicTable({ onClose }: { onClose: () => void }) {
  return (
    <div className="exam-window" role="dialog" aria-modal="true" aria-label="Periodic table">
      <div className="exam-window-head">
        <h2>Periodic Table of the Elements</h2>
        <button type="button" onClick={onClose} className="exam-window-close">
          Close
        </button>
      </div>
      <div className="exam-window-body">
        <div className="pt-grid">
          {ELEMENTS.map(([number, symbol, weight, row, column]) => (
            <div key={number} style={{ gridRow: row, gridColumn: column }}>
              <Cell number={number} symbol={symbol} weight={weight} />
            </div>
          ))}
        </div>
        <div className="pt-series">
          <div className="pt-series-row">
            <span>Lanthanides</span>
            {LANTHANIDES.map(([number, symbol, weight]) => (
              <Cell key={number} number={number} symbol={symbol} weight={weight} />
            ))}
          </div>
          <div className="pt-series-row">
            <span>Actinides</span>
            {ACTINIDES.map(([number, symbol, weight]) => (
              <Cell key={number} number={number} symbol={symbol} weight={weight} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
