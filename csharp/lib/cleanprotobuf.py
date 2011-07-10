"""\
cleanprotobuf reads a C# file generated by ProtoGen.exe and fixes/removes
all references to protobuf-csharp assemblies to avoid unnecessary dependencies.
As of now, phone metadata is read from the source XML file and not from
the protocol buffers files.
"""
import sys, os, re

replacements = [
    # Remove using directives
    (r'\nusing .*?Google.ProtocolBuffers.*?;', '', re.S),
    # Remove RegisterAllExtensions
    (r'#region Extension registration.*?#endregion', '', re.S),
    # Remove GeneratedMessageLite inheritance
    (r'\s*:\s*pb::[a-zA-Z0-9]+<[^>]+>', '', re.S),
    # Remove WriteTo()
    (r'\n    public override void WriteTo.*?\n    }', '', re.S),
    # Remove SerializedSize
    (r'\n    public override int SerializedSize.*?\n    }', '', re.S),
    # Remove ParseFrom
    (r'\n    public static \w+ ParseFrom.*?\n    }', '', re.S),
    # Remove ParseFrom
    (r'\n    public static \w+ ParseDelimitedFrom.*?\n    }', '', re.S),
    (r'\n      public override Builder MergeFrom\(pb\:\:.*?\n      }', '', re.S),
    (r'\n    public override void PrintTo.*?\n    }', '', re.S),
    (r'pbc::PopsicleList<([^>]+)>', r'scg::List<\1>', None),
    (r'pbc::IPopsicleList<([^>]+)>', r'scg::IList<\1>', None),
    (r'pb::ThrowHelper.ThrowIfNull\(([^,]+), ([^\)]+)\);',
         r'if(\1 == null) throw new global::System.ArgumentNullException(\2);',
         None),

    (r'(public|protected|private)\s+override\s+(?!.*(?:GetHashCode|Equals))', r'\1 ', None),
    (r'public sealed partial class', 'public partial class', None),
    (r'\n(\s+)public\s+(\S+)\s+BuildPartial\(\)',
         r'\n\1public \2 Build() { return BuildPartial(); }\n\1public \2 BuildPartial()',
         re.S),

    (r'pbc::Lists.AsReadOnly\(([^\)]+)\)', r'\1', None),

    (r'\n\s*result[^\n]+MakeReadOnly\(\);', '\n', re.S),
    (r'base\.AddRange\(([^,]+),([^\)]+)\);', r'\2.AddRange(\1);', None),
    (r'private int memoizedSerializedSize = -1;', '', None),
]


def cleanlines(data):
    for pattern, repl, reopts in replacements:
        r = re.compile(pattern, reopts or 0)
        data = r.sub(repl, data)
    return data

if __name__ == '__main__':
    input, output = sys.argv[1:3]
    data = file(input, 'r').read()
    data = cleanlines(data)
    file(output, 'w').write(data)