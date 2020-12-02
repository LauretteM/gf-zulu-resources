--# -path=$ZUL_RG/abstract

abstract Test =
  Grammar,
  Backward[ComplV2,ComplV3],
  ExtraCatZulAbs,
  ExtraZulAbs,
  TestLex,
  Symbol,
  TempAbs

  ** {
  flags startcat=Phr ;
  } ;
