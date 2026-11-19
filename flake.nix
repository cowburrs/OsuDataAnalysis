{
  description = "osuscrape";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs =
    { self, nixpkgs }:
    let
      pkgs = nixpkgs.legacyPackages.x86_64-linux;

      python = pkgs.python3.withPackages (
        ps: with ps; [
          matplotlib
          pandas
          requests
          zstandard
          huggingface-hub
          pyarrow
          tqdm
          ossapi
          ratelimit
        ]
      );

      snapshot = pkgs.writeShellScript "snapshot" ''
        exec ${python}/bin/python ${./src/osu.py} "$@"
      '';
    in
    {
      devShells.x86_64-linux.default = pkgs.mkShell {
        packages = [
          python
          pkgs.pyright
          pkgs.isort
          pkgs.black
        ];
        shellHook = ''
          export PS1="\n\[\033[1;32m\][nix-shell:\w]\$\[\033[0m\] "
        '';
      };

      apps.x86_64-linux.default = {
        type = "app";
        program = "${snapshot}";
      };
    };
}
